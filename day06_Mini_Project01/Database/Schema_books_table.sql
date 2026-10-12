CREATE SCHEMA bookworm_db;


USE bookworm_db;

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    status ENUM('Want to Read', 'Reading', 'Completed')
        NOT NULL DEFAULT 'Want to Read',
    cover TEXT
);

DESCRIBE books;
SHOW tables;
