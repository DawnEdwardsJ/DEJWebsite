/**
 * Cloudflare Workers entry point. The site itself is served as static assets
 * from _site/; only /api/* reaches this code (see run_worker_first in
 * wrangler.jsonc). The enquiry handler is shared with the Pages Functions
 * version in functions/api/enquiry.js, so either hosting setup works.
 */
import { onRequestPost, onRequest } from "../functions/api/enquiry.js";

export default {
  async fetch(request, env, ctx) {
    const { pathname } = new URL(request.url);
    if (pathname === "/api/enquiry") {
      return request.method === "POST" ? onRequestPost({ request, env, ctx }) : onRequest();
    }
    return env.ASSETS.fetch(request);
  },
};
