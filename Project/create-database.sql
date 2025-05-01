CREATE DATABASE securityincidenttracker;

CREATE USER sit_admin WITH PASSWORD 'pass';

GRANT ALL PRIVILEGES ON DATABASE securityincidenttracker TO sit_admin;
