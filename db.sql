create database if not exists automation_db;
use automation_db;

CREATE TABLE report_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    value VARCHAR(100)
);