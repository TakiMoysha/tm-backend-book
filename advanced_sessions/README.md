# Elysia with Bun runtime

```bash
bun run dev
```

## Context File

**Routing**:

- methods;
- context (params, query, headers, cookie, body);
- params;

**Decorate**:

- di;

**Validation**:

- buildin `t`;
- swagger integration (request, response, params, models, ...);
-

**Plugins**:
- ex. swagger;

```ts
class Account {
  constructor(public email: string) {}
}

const app = new Elysia()
  .use(swagger())
  .decorate("account", Account)
  .get("/account", ({ account }) => account.email)
  .get(
    "/account/:id",
    ({ account, params, { id }, error }) => account.name ?? error(404, "custom message"),
    { params: t.Object({ id: t.String() }) }
  )
  .get("/path", (ctx) => {})
  .post("/path", { path, ... }) => {})
  .put("/path/:id", { params: { id }} => { params })
  .delete("/path", )
```

# Bibliography

1. [Official Documentation / elysiajs.com](https://elysiajs.com/tutorial.html)
2.
