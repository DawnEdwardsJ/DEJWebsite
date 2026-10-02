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
  // No-JavaScript fallback: send the visitor back to the form with a result flag.
  const url = new URL("/contact/", request.url);
  url.searchParams.set("enquiry", ok ? "sent" : "error");
  url.hash = "enquire";
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
    throw new Error(`Tekmatix ${path} ${res.status}: ${text.slice(0, 300)}`);
  }
  return res.json().catch(() => ({}));
}

export async function onRequestPost({ request, env }) {
  let form;
  try {
    form = Object.fromEntries(await request.formData());
  } catch {
    return reply(request, false);
  }

  // Honeypot: real people never see or fill this field.
  if (clean(form.company_website, 200)) return reply(request, true);

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

  if (!env.TEKMATIX_API_TOKEN) {
    console.error("TEKMATIX_API_TOKEN is not set; enquiry not delivered", { email, type: type.value });
    return reply(request, false, 503);
  }

  const locationId = env.TEKMATIX_LOCATION_ID || enquiry.locationId;
  try {
    const upsert = await tekmatix(env, "/contacts/upsert", {
      locationId,
      firstName,
      lastName: lastName || undefined,
      email,
      phone: phone || undefined,
      source: enquiry.source,
    });
    const contactId = upsert?.contact?.id;
    if (!contactId) throw new Error("Tekmatix upsert returned no contact id");

    // Tags are added separately so existing tags on a returning contact are kept.
    await tekmatix(env, `/contacts/${contactId}/tags`, {
      tags: [...enquiry.baseTags, ...type.tags],
    });
    const header = [`Website enquiry: ${type.label}`];
    if (page) header.push(`Sent from: ${enquiry.source}${page}`);
    if (phone) header.push(`Phone: ${phone}`);
    await tekmatix(env, `/contacts/${contactId}/notes`, {
      body: `${header.join("\n")}\n\n${message || "(no message)"}`,
    });
  } catch (err) {
    console.error(String(err));
    return reply(request, false, 502);
  }

  return reply(request, true);
}

export function onRequest() {
  return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
}
