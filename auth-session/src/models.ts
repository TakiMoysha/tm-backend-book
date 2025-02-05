export interface ISession {
  id: string;
  accountId: number;
  createdAt: Date;
  expiredAt: Date;
}

export interface IAccount {
  id: number;
}
