import Elysia from "elysia";
import { sql } from "~/db";
import { createSession, generateSesionToken } from "~/services/auth.session";
// import { handlerSignIn } from "~/services/auth.service";

export interface AuthPluginOptions {}

const defaultOptions: AuthPluginOptions = {};

export const AuthPlugin = (opts: AuthPluginOptions = defaultOptions) => {
  if (!Object.is(opts, defaultOptions)) {
    opts = { ...defaultOptions, ...opts };
  }

  return new Elysia({ prefix: "/auth" })
    .decorate("options", opts)
    .decorate("db", sql)
    .post("/sign-in", async ({ set, request, options, body, db }) => {
      console.log("[DEBUG] sign-in: ", request, options, body);
      const token = generateSesionToken();
      const session = await createSession(token, 1, { db });
      set.headers["set-cookie"] =
        `x-session=${session.id}; path=/; httponly; secure; samesite=lax`;
      return { "x-session": session.id, token, user: { id: 1 } };
    })
    .post("/sign-up", ({ request, options, body }) => {
      console.log("[DEBUG] sign-up");
    })
    .post("/sign-out", ({ request, options, body }) => {
      console.log("[DEBUG] sign-out");
    });
};
