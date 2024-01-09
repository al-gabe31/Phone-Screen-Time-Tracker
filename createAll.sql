CREATE TABLE IF NOT EXISTS Entry (
    entry_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    date_str DATE,
    UNIQUE (date_str)
);

CREATE TABLE IF NOT EXISTS App_List (
    app_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name VARCHAR(50),
    UNIQUE (app_name)
);

CREATE TABLE IF NOT EXISTS App_Data (
    app_data_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_ID INTEGER,
    app_name VARCHAR(50),
    time_duration INTEGER NOT NULL,
    FOREIGN KEY (entry_ID) REFERENCES Entry(entry_ID),
    FOREIGN KEY (app_name) REFERENCES App_List(app_name)
);