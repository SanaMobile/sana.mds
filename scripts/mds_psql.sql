CREATE DATABASE mds;
CREATE USER mds WITH PASSWORD 'password';
ALTER ROLE mds SET client_encoding TO 'utf8';
ALTER ROLE mds SET default_transaction_isolation TO 'read committed';
ALTER ROLE mds SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mds TO mds;
