import { sql } from "./db";
import { fileURLToPath } from "bun";
import shift from "postgres-shift";

const path = fileURLToPath(new URL("migrations", import.meta.url));

shift({
  sql,
  path,
  before: ({ migration_id, name }) => {
    console.log(`[MIGRATION] ${migration_id} ${name}`);
  },
})
  .then(() => console.log("done"))
  .catch((err: Error) => {
    console.error("FAILED", err);
    process.exit(1);
  });
