export interface ISession {
  id: string;
  accountId: number;
  createdAt: Date;
  expiredAt: Date;
}

export interface IAccount {
  id: number;
  email: string;
  password: string;
  lastLogin: Date;
  createdAt: Date;
  isVerified: boolean;
  isActive: boolean;
  isStaff: boolean;
  isAdmin: boolean;
  isSuperuser: boolean;
}
