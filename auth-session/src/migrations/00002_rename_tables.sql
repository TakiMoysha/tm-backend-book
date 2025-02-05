ALTER TABLE users RENAME TO account;
ALTER TABLE session RENAME COLUMN users_id TO account_id;

