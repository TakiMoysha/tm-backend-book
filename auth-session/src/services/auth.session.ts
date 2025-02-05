import { type sql } from "../db";
import { ISession, IAccount } from "../models";
import { encodeBase32LowerCaseNoPadding } from "@oslojs/encoding";
import { newSessionId } from "./auth.helpers";

const SessionTTL = 1000 * 60 * 60 * 24;

export type SessionValidationResult =
  | { session: ISession; account: IAccount }
  | { session: null; account: null };

export const generateSesionToken = (): string => {
  const bytes = new Uint8Array(20);
  crypto.getRandomValues(bytes);
  return encodeBase32LowerCaseNoPadding(bytes);
};

export const createSession = async (
  token: string,
  accountId: number,
  { db }: { db: typeof sql },
): Promise<ISession> => {
  if (!process.env.SECRET_KEY) console.error("SECRET_KEY is not defined");

  const session = {
    id: newSessionId(token),
    accountId,
    createdAt: new Date(),
    expiredAt: new Date(Date.now() + SessionTTL),
  };

  console.log(`[DEBUG] prepare session: ${JSON.stringify(db(session))}`);
  await db`
    INSERT INTO session 
      ${db(session, "id", "accountId", "createdAt", "expiredAt")}
    RETURNING id, user_id;`;

  console.log("[DEBUG] created session: ", session);
  return session;
};

export const validateSessionToken = async (
  token: string,
  { db }: { db: typeof sql },
): Promise<SessionValidationResult> => {
  // does the session exists in the database?
  const sessionId = newSessionId(token);
  const row = await db<ISession[]>`
  SELECT(
    account.id,
    account.user_id,
    account.created_at,
    account.expired_at
  )
    FROM session 
    WHERE session.id = ${sessionId} `;

  if (!row.length) {
    return { session: null, account: null };
  }

  console.log("[DEBUG] user row: ", row);
  const session = row[0];

  const user: IAccount = {
    id: session.accountId,
  };

  // is the session expired?
  if (Date.now() >= session.expiredAt.getTime()) {
    await db`DELETE FROM sessions WHERE id = ${session.id} `;
    return { session: null, account: null };
  }
  if (Date.now() >= session.expiredAt.getTime() - SessionTTL / 2) {
    session.expiredAt = new Date(Date.now() + SessionTTL);
    await db`UPDATE session SET expired_at = ${session.expiredAt} WHERE id = ${session.id} `;
  }

  return { session, account: user };
};
