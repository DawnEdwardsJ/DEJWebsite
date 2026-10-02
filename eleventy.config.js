import { eleventyImageTransformPlugin } from "@11ty/eleventy-img";
import markdownIt from "markdown-it";
import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";
import buildOgImages from "./og/build-og.js";

export default function (eleventyConfig) {
  // ---- Markdown: used for page bodies and for every text field in the CMS.
  // `html: true` so the occasional <em> or <br> typed by hand still works.
  const md = markdownIt({ html: true, linkify: false, typographer: false });
  eleventyConfig.setLibrary("md", md);

  // Block Markdown (paragraphs, lists) for longer text fields.
  eleventyConfig.addFilter("md", (value) => (value ? md.render(String(value)) : ""));
  // Inline Markdown (*italic*, **bold**, links) for headings and one-liners.
  eleventyConfig.addFilter("mdi", (value) => (value ? md.renderInline(String(value)) : ""));
  // Line breaks typed in the CMS become <br>.
  eleventyConfig.addFilter("lines", (value) =>
    value ? String(value).split(/\n+/).map((l) => md.renderInline(l.trim())).join("<br>") : ""
  );

  // Links to the New Dawn Wellness site are hidden until that site is live.
  // One switch in Site settings (wellnessSiteLive) brings them all back.
  let site = {};
  eleventyConfig.on("eleventy.before", () => {
    site = JSON.parse(fs.readFileSync("src/_data/site.json", "utf8"));
  });
  const isLive = (href) =>
    !href || site.wellnessSiteLive || !String(href).startsWith(site.wellnessUrl);
  eleventyConfig.addFilter("linkIsLive", isLive);
  eleventyConfig.addFilter("liveLinks", (items, key = "link") =>
    Array.isArray(items) ? items.filter((it) => isLive(it?.[key])) : []
  );

  // Buttons left half-filled in the CMS are skipped rather than shown empty.
  eleventyConfig.addFilter("usable", (items) =>
    Array.isArray(items) ? items.filter((b) => b && b.label && b.link) : []
  );
  eleventyConfig.addFilter("containsUrl", (items, url) =>
    Array.isArray(items) && items.some((it) => it?.link === url)
  );
  // Tiny blurred previews shown behind each photo while it loads (~300 bytes each).
  // Built for every image under src/images, so newly uploaded photos get one too.
  const lqip = new Map();
  eleventyConfig.on("eleventy.before", async () => {
    const root = "src/images";
    const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
      e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]);
    const files = walk(root).filter((f) => /\.(jpe?g|png|webp)$/i.test(f) && !f.includes(`${path.sep}logos${path.sep}`));
    await Promise.all(files.map(async (file) => {
      const key = "/" + path.relative("src", file).split(path.sep).join("/");
      const stat = fs.statSync(file);
      const cached = lqip.get(key);
      if (cached && cached.mtime === stat.mtimeMs) return;
      const buf = await sharp(file).resize(24).blur(1.2).webp({ quality: 40 }).toBuffer();
      lqip.set(key, { mtime: stat.mtimeMs, uri: `data:image/webp;base64,${buf.toString("base64")}` });
    }));
  });
  eleventyConfig.addFilter("lqip", (src) => lqip.get(src)?.uri || "");

  eleventyConfig.addFilter("json", (value) => JSON.stringify(value));
  eleventyConfig.addFilter("year", () => new Date().getFullYear());

  // ---- Static files copied as-is.
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "src/og-image.jpg": "og-image.jpg" });
  eleventyConfig.addPassthroughCopy({ "src/_headers": "_headers" });
  eleventyConfig.addPassthroughCopy({ "src/_redirects": "_redirects" });

  // ---- Images: every <img> pointing at a local file is resized and served as
  // WebP with a JPEG fallback, with width/height set so the page doesn't jump.
  eleventyConfig.addPlugin(eleventyImageTransformPlugin, {
    formats: ["svg", "webp", "jpeg"],
    svgShortCircuit: true,
    widths: [480, 800, 1200, 1600],
    sharpWebpOptions: { quality: 74 },
    sharpJpegOptions: { quality: 78, mozjpeg: true, progressive: true },
    htmlOptions: {
      imgAttributes: { loading: "lazy", decoding: "async" },
    },
  });

  // Branded share card per page (og/build-og.js), written to _site/og/<page>.jpg
  eleventyConfig.on("eleventy.after", async ({ dir }) => buildOgImages(dir.output));
  eleventyConfig.addFilter("ogImage", (url) => {
    const slug = String(url || "/").replace(/^\/|\/$/g, "") || "home";
    return /^[a-z0-9-]+$/.test(slug) && fs.existsSync(`src/pages/${slug === "home" ? "index" : slug}.md`)
      ? `/og/${slug}.jpg`
      : "/og-image.jpg";
  });

  eleventyConfig.addWatchTarget("src/assets/");

  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
}
