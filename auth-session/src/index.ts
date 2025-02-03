import { Elysia } from "elysia";
import { swagger } from "@elysiajs/swagger";

import { AuthPlugin } from "./plugins/auth";

const app = new Elysia()
  .use(swagger())
  .use(AuthPlugin())
  .get("/*", () => {})
  .listen(3000);

console.log(`🦊 Start at ${app.server?.hostname}:${app.server?.port}`);
