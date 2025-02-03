export interface ISession {
  id: string;
  userId: number;
  createdAt: Date;
  expiresAt: Date;
}

export interface IUser {
  id: number;
}
