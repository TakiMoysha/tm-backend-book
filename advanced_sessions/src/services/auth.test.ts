import { sql } from "../db";
import { describe, expect, it, jest } from "bun:test";
import {
  generateSesionToken,
  createSession,
  validateSessionToken,
} from "./auth.session";

describe("auth:session", () => {
  const ids = [3123, 1521, 48124, 598125];
  const setCookies = jest.fn((cookies: { "x-session": string }) => { });
  const getTokenFromRequest = jest.fn(() => generateSesionToken());

  it.each(ids)("should create session", async (accountId) => {
    const token = generateSesionToken();
    const session = await createSession(token, accountId, { db: sql });
    expect(session).toBeTruthy();
  });

  it("should validate session", async () => {
    const token = generateSesionToken();
    const result = await validateSessionToken(token, { db: sql });
    expect(result).toBeTruthy();
  });

  it.skip("use-case: set cookies", async () => {
    const token = generateSesionToken();
    const session = await createSession(token, 1, { db: sql });
    setCookies({ "x-session": session.id });
  });

  it.skip("use-case: validate session", async ({ }) => {
    const token = getTokenFromRequest();
    const result = await validateSessionToken(token, { db: sql });
    if (result.session === null) {
      console.error("Invalid session!");
    }
  });
});

describe("auth:account", () => { });
