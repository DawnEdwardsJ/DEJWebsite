/**
 * Branded social share cards (1200x630), one per page, built from each page's
 * opening banner: its photo, small label and heading. Written to _site/og/.
 *
 * Runs after every Eleventy build. Cards are cached by content, so only pages
 * whose banner changed are redrawn.
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import matter from "gray-matter";
import satori from "satori";
import sharp from "sharp";

const W = 1200;
const H = 630;
const NAVY = "#192b53";
const CREAM = "#ffead1";
const GOLD = "#f4a261";
const BEIGE = "#e9cba7";
const DEFAULT_PHOTO = { photo: "/images/photos/dawn-writing-smile.jpg", photo_position: "center top" };
const CACHE = ".cache/og";

const font = (file) => fs.readFileSync(new URL(`./fonts/${file}`, import.meta.url));
const fonts = [
  { name: "Cormorant", data: font("cormorant-garamond-500.ttf"), weight: 500, style: "normal" },
  { name: "Cormorant", data: font("cormorant-garamond-500-italic.ttf"), weight: 500, style: "italic" },
  { name: "Montserrat", data: font("montserrat-500.ttf"), weight: 500, style: "normal" },
  { name: "Montserrat", data: font("montserrat-600.ttf"), weight: 600, style: "normal" },
];

// Satori lays out with flexbox only, so every div is a flex container.
const el = (type, style, children) => ({
  type,
  props: { style: type === "div" ? { display: "flex", ...style } : style, children },
});

// "From overwhelm to *calm, embodied leadership.*" -> spans with the starred part in italic gold
function headingSpans(text) {
  return String(text)
    .split(/(\*[^*]+\*)/)
    .filter(Boolean)
    .map((part) =>
      part.startsWith("*")
        ? el("span", { fontStyle: "italic", color: GOLD }, part.slice(1, -1))
        : el("span", {}, part)
    );
}

function pageInfo(file) {
  const data = matter.read(file).data;
  const sections = data.sections || [];
  const hero = sections.find((s) => s.type === "hero" || s.type === "hero_photo") || {};
  const source = hero.photo ? hero : sections.find((s) => s.photo) || DEFAULT_PHOTO;
  const slug = path.basename(file, ".md");
  return {
    out: slug === "index" ? "home" : slug,
    kicker: hero.kicker || "",
    heading: hero.heading || String(data.title || "").split("|")[0].trim(),
    photo: source.photo,
    position: source.photo_position || "center",
  };
}

const PHOTO_W = 500;

// CSS object-position ("center top", "70% center", "30% 20%") -> sharp crop gravity
function gravity(position = "") {
  const [x = "center", y = "center"] = String(position).trim().split(/\s+/);
  const pct = (v, lo, hi) => (/%$/.test(v) ? (parseFloat(v) < 40 ? lo : parseFloat(v) > 60 ? hi : "") : v === lo || v === hi ? v : "");
  const h = pct(x, "left", "right");
  const v = pct(y, "top", "bottom");
  const map = { top: "north", bottom: "south", left: "west", right: "east" };
  if (!h && !v) return "attention";
  return (map[v] || "") + (map[h] || "") || "attention";
}

async function photoDataUri(src, position) {
  const file = path.join("src", src);
  const pos = gravity(position);
  const buf = await sharp(file).resize(PHOTO_W, H, { fit: "cover", position: pos }).jpeg({ quality: 82 }).toBuffer();
  return `data:image/jpeg;base64,${buf.toString("base64")}`;
}

async function render(info) {
  const len = info.heading.replace(/\*/g, "").length;
  const size = len > 48 ? 54 : len > 32 ? 62 : 72;
  const tree = el("div", { width: W, height: H, display: "flex", position: "relative", backgroundColor: NAVY }, [
    // portrait photo panel on the right, softened into the navy at its left edge
    {
      type: "img",
      props: { src: await photoDataUri(info.photo, info.position), width: PHOTO_W, height: H, style: { position: "absolute", right: 0, top: 0 } },
    },
    el("div", {
      position: "absolute", right: PHOTO_W - 160, top: 0, width: 160, height: H,
      backgroundImage: "linear-gradient(90deg, rgba(25,43,83,1) 0%, rgba(25,43,83,0) 100%)",
    }, []),
    el("div", { position: "absolute", left: 80, top: 0, width: 600, height: H, flexDirection: "column", justifyContent: "center" }, [
      info.kicker
        ? el("div", { display: "flex", alignItems: "center", marginBottom: 26 }, [
            el("div", { width: 34, height: 2, backgroundColor: GOLD, marginRight: 16 }, []),
            el("div", { fontFamily: "Montserrat", fontWeight: 600, fontSize: 20, letterSpacing: 5, color: GOLD, textTransform: "uppercase" }, info.kicker.replace(/\*/g, "")),
          ])
        : el("div", { display: "flex" }, []),
      el("div", { display: "flex", flexWrap: "wrap", fontFamily: "Cormorant", fontWeight: 500, fontSize: size, lineHeight: 1.08, color: CREAM }, headingSpans(info.heading)),
    ]),
    el("div", { position: "absolute", left: 80, bottom: 52, display: "flex", alignItems: "center" }, [
      el("div", { fontFamily: "Cormorant", fontWeight: 500, fontSize: 30, color: CREAM, marginRight: 22 }, "Dawn Edwards-Jones"),
      el("div", { width: 1, height: 22, backgroundColor: "rgba(255,234,209,0.4)", marginRight: 22 }, []),
      el("div", { fontFamily: "Montserrat", fontWeight: 500, fontSize: 17, letterSpacing: 3, color: BEIGE, textTransform: "uppercase" }, "dawnedwards-jones.com"),
    ]),
  ]);
  const svg = await satori(tree, { width: W, height: H, fonts });
  return sharp(Buffer.from(svg)).jpeg({ quality: 84, mozjpeg: true }).toBuffer();
}

export default async function buildOgImages(outputDir) {
  const dir = "src/pages";
  fs.mkdirSync(path.join(outputDir, "og"), { recursive: true });
  fs.mkdirSync(CACHE, { recursive: true });
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".md"));
  await Promise.all(files.map(async (f) => {
    const info = pageInfo(path.join(dir, f));
    const photoStat = fs.statSync(path.join("src", info.photo)).mtimeMs;
    const key = crypto.createHash("sha1").update(JSON.stringify([info, photoStat, 5])).digest("hex").slice(0, 16);
    const cached = path.join(CACHE, `${info.out}-${key}.jpg`);
    if (!fs.existsSync(cached)) fs.writeFileSync(cached, await render(info));
    fs.copyFileSync(cached, path.join(outputDir, "og", `${info.out}.jpg`));
  }));
}
