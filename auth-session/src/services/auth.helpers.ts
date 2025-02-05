import { encodeHexLowerCase } from "@oslojs/encoding";

// ================================== WRAPPERS
export const newSessionId = (token: string): string =>
  encodeHexLowerCase(
    new Bun.CryptoHasher("sha256", process.env?.SECRET_KEY ?? "")
      .update(token)
      .digest(),
  );

// ================================== MONADS
