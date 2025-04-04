CREATE TABLE urls (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    url        TEXT NOT NULL,
    first_view DATETIME NULL,
    last_view  DATETIME NULL
);