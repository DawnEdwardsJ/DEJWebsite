/**
 * POST /api/enquiry
 *
 * Receives the contact form and creates (or updates) the contact in Tekmatix,
 * tags it by enquiry type, and attaches the message as a note. Tekmatix
 * workflows triggered by those tags do the rest (pipeline, notifications,
 * any confirmation email).
 *
 * Needs one secret in Cloudflare Pages → Settings → Environment variables:
 *   TEKMATIX_API_TOKEN   Private Integration token (Tekmatix → Settings →
 *                        Private Integrations) with contacts read/write scope.
 * Optional:
 *   TURNSTILE_SECRET_KEY Cloudflare Turnstile secret. When set (together with
 *                        turnstileSiteKey in src/_data/site.json) every
 *                        submission must pass the Turnstile check.
 *   TEKMATIX_LOCATION_ID defaults to the location in src/_data/enquiry.json
 *   TEKMATIX_API_BASE    only for local testing against a mock server
 *
 * Until the token is set, the form tells visitors to email instead, so no
 * enquiry is silently lost.
 */
import enquiry from "../../src/_data/enquiry.json";

const DEFAULT_API = "https://services.leadconnectorhq.com";
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function clean(value, max) {
  return String(value ?? "").trim().slice(0, max);
}

function reply(request, ok, status = ok ? 200 : 400) {
  const accept = request.headers.get("accept") || "";
  if (accept.includes("application/json")) {
    return new Response(JSON.stringify({ ok }), {
      status,
      headers: { "content-type": "application/json", "cache-control": "no-store" },
    });
  }
  // No-JavaScript fallback: back to the form, where :target shows the result message.
  const url = new URL("/contact/", request.url);
  url.hash = ok ? "enquiry-sent" : "enquiry-error";
  return Response.redirect(url.toString(), 303);
}

async function tekmatix(env, path, body) {
  const res = await fetch((env.TEKMATIX_API_BASE || DEFAULT_API) + path, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.TEKMATIX_API_TOKEN}`,
      Version: "2021-07-28",
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    const err = new Error(`Tekmatix ${path} ${res.status}: ${text.slice(0, 300)}`);
    err.status = res.status;
    throw err;
  }
  return res.json().catch(() => ({}));
}

async function passesTurnstile(env, form, request) {
  if (!env.TURNSTILE_SECRET_KEY) return true;
  const body = new FormData();
  body.append("secret", env.TURNSTILE_SECRET_KEY);
  body.append("response", String(form["cf-turnstile-response"] || ""));
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) body.append("remoteip", ip);
  try {
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
    const data = await res.json();
    return Boolean(data.success);
  } catch (err) {
    console.error("Turnstile check failed to run", String(err));
    return false;
  }
}

export async function onRequestPost({ request, env }) {
  let form;
  try {
    form = Object.fromEntries(await request.formData());
  } catch {
    return reply(request, false);
  }

  // Honeypot: hidden from people, so anything in it is almost certainly a bot.
  // Logged rather than silently dropped, in case a browser autofilled it.
  if (clean(form.nd_check, 200)) {
    console.warn("Honeypot filled; enquiry not sent to Tekmatix", { email: clean(form.email, 160) });
    return reply(request, true);
  }
  if (!(await passesTurnstile(env, form, request))) return reply(request, false, 403);

  const firstName = clean(form.first_name, 80);
  const lastName = clean(form.last_name, 80);
  const email = clean(form.email, 160).toLowerCase();
  const phone = clean(form.phone, 40);
  const message = clean(form.message, 5000);
  const page = clean(form.page, 200);
  if (!firstName || !EMAIL_RE.test(email)) return reply(request, false);

  const type =
    enquiry.types.find((t) => t.value === form.enquiry_type) ||
    enquiry.types[enquiry.types.length - 1];

  // Everything needed to follow up by hand if Tekmatix can't be reached.
  const record = { firstName, lastName, email, phone, type: type.value, page, message };

  if (!env.TEKMATIX_API_TOKEN) {
    console.error("TEKMATIX_API_TOKEN is not set; enquiry not delivered", record);
    return reply(request, false, 503);
  }

  const locationId = env.TEKMATIX_LOCATION_ID || enquiry.locationId;
  try {
    const contact = { locationId, firstName, lastName: lastName || undefined, email };
    let upsert;
    try {
      upsert = await tekmatix(env, "/contacts/upsert", { ...contact, phone: phone || undefined });
    } catch (err) {
      // A phone number Tekmatix can't parse shouldn't cost us the lead.
      if (!phone || ![400, 422].includes(err.status)) throw err;
      upsert = await tekmatix(env, "/contacts/upsert", contact);
    }
    const contactId = upsert?.contact?.id;
    if (!contactId) throw new Error("Tekmatix upsert returned no contact id");

    // Note first, tags last: tags trigger Tekmatix workflows, so by the time a
    // workflow runs the message is already on the contact.
    const header = [`Website enquiry: ${type.label}`];
    if (page) header.push(`Sent from: ${enquiry.source}${page}`);
    if (phone) header.push(`Phone: ${phone}`);
    await tekmatix(env, `/contacts/${contactId}/notes`, {
      body: `${header.join("\n")}\n\n${message || "(no message)"}`,
    });
    // Tags are added separately so existing tags on a returning contact are kept.
    await tekmatix(env, `/contacts/${contactId}/tags`, {
      tags: [...enquiry.baseTags, ...type.tags],
    });
  } catch (err) {
    console.error("Enquiry not fully delivered to Tekmatix", String(err), record);
    return reply(request, false, 502);
  }

  return reply(request, true);
}

export function onRequest() {
  return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
}
