import { type sql } from "../db";
import { ISession, IUser } from "../models";
import { encodeBase32LowerCaseNoPadding } from "@oslojs/encoding";
import { newSessionId } from "./auth.helpers";

const SessionTTL = 1000 * 60 * 60 * 24;

export type SessionValidationResult =
  | { session: ISession; user: IUser }
  | { session: null; user: null };

export const generateSesionToken = (): string => {
  const bytes = new Uint8Array(20);
  crypto.getRandomValues(bytes);
  return encodeBase32LowerCaseNoPadding(bytes);
};

export const createSession = async (
  token: string,
  userId: number,
  { db }: { db: typeof sql },
): Promise<ISession> => {
  if (!process.env.SECRET_KEY) console.error("SECRET_KEY is not defined");

  const session = {
    id: newSessionId(token),
    userId,
    createdAt: new Date(),
    expiresAt: new Date(Date.now() + SessionTTL),
  };

  await db`
    INSERT INTO
      sessions (id, user_id, created_at, expires_at)
    VALUES (${db(session)})`;

  return session;
};

export const validateSessionToken = async (
  token: string,
  { db }: { db: typeof sql },
): Promise<SessionValidationResult> => {
  // does the session exists in the database?
  const sessionId = newSessionId(token);
  const row = await db<ISession[]>`
    SELECT (
      user_sesssion.id,
      user_session.user_id,
      user_session.created_at,
      user_session.expires_at
    )
    FROM user_session
    WHERE user_session.id = ${sessionId}`;

  if (!row.length) {
    return { session: null, user: null };
  }

  console.log("[DEBUG] user row: ", row);
  const session = row[0];

  const user: IUser = {
    id: session.userId,
  };

  // is the session expired?
  if (Date.now() >= session.expiresAt.getTime()) {
    await db`DELETE FROM sessions WHERE id = ${session.id}`;
    return { session: null, user: null };
  }
  if (Date.now() >= session.expiresAt.getTime() - SessionTTL / 2) {
    session.expiresAt = new Date(Date.now() + SessionTTL);
    await db`UPDATE user_session SET expires_at = ${session.expiresAt} WHERE id = ${session.id}`;
  }

  return { session, user };
};
