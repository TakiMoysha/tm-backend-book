declare module "postgres-shift" {
  import { Sql } from "postgres";

  export default async (options: {
    sql: Sql;
    path?: string;
    before?: Promise<{ migration_id: number; name: string }>;
    after?: ;
  }): Promise<unjnown> => { };
}
