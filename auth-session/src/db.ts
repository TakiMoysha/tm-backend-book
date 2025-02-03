import postgres from "postgres";

export const sql = postgres({
  db: "auth_session",
  debug: true,
  username: "postgres",
  password: "postgres",
  idle_timeout: 1,
});
