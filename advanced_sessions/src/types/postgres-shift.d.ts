declare module "postgres-shift" {
  import { Sql } from "postgres";

  interface HooksParams {
    migration_id: string;
    name: string;
  }

  export default async (options: {
    sql: Sql;
    path?: string;
    before?: (opts: HooksParams) => void | Promise<void>;
    after?: () => void | Promise<void>;
  }): Promise<unjnown> => { };
}
