import { describe, it, expect } from "bun:test";
import { sql } from "./db";

describe("db", () => {
  it("should connect to the database", async () => {
    const result = await sql`SELECT 1 + 1`;
    expect(result[0].sum).toBe(2);
  });
});
