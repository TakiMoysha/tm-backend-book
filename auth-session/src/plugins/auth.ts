import Elysia from "elysia";

export interface AuthPluginOptions { }

const defaultOptions: AuthPluginOptions = {};

export const AuthPlugin = (opts: AuthPluginOptions = defaultOptions) => {
  if (!Object.is(opts, defaultOptions)) {
    opts = { ...defaultOptions, ...opts };
  }

  return new Elysia({ prefix: "/auth" })
    .decorate("options", opts)
    .post("/sign-in", () => { })
    .post("/sign-up", () => { })
    .post("/sign-out", () => { });
};
