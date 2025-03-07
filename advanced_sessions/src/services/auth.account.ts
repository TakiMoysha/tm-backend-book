import { sql } from "~/db";
import { IAccount } from "~/models";

export const authenticate = (
  body: { email: string },
  opts: { db: typeof sql },
) => {
  const user = sql<IAccount>`SELECT * FROM account WHERE email = ${body.email}`;
  if (!user)
    return {
      id: 1,
      email: body.email,
    };
};
