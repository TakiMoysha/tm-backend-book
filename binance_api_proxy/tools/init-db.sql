-- Initialize TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create hypertable for trade_ticks
-- This will be done after table creation by the application
-- But we can prepare the database here

-- Enable TimescaleDB features
SELECT timescaledb_pre_restore();

-- You can add any initial setup here

SELECT timescaledb_post_restore();
