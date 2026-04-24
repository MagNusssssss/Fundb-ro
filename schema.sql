DROP TABLE IF EXISTS Fundsachen;

CREATE TABLE Fundsachen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    description TEXT,
    found_date DATE NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL
);


