PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);


CREATE TABLE IF NOT EXISTS Sobstvenik (
    id integer primary key AUTOINCREMENT,
    name varchar,
    phone_number varchar
);

create TABLE IF NOT EXISTS Kvartiras (
    id integer primary key AUTOINCREMENT,
    adres varchar,
    url text NOT NULL
);

DROP TABLE IF EXISTS Kvartiras;

CREATE TABLE Kvartiras2 (
    id integer PRIMARY KEY AUTOINCREMENT,
    adres varchar,
    image_part NOT NULL, 
    url text NOT NULL
);

create TABLE IF NOT EXISTS Kvartira (
    id integer primary key AUTOINCREMENT,
    adres varchar,
    cena integer,
    rooms integer,
    SobstvenikId integer,
    foreign key (SobstvenikId) references Sobstvenik(id)
);

create Table IF NOT EXISTS client(
    id integer primary key AUTOINCREMENT,
    name varchar,
    phone_number varchar
);

create Table IF NOT EXISTS Zayavka(
    id integer primary key AUTOINCREMENT,
    zhelaemyi_adres varchar,
    zhelaemyi_cena integer,
    kol_vo_rooms integer,
    satus varchar,
    KvartiraId integer,
    clientId integer,
    foreign key (clientId) references client(id)
    foreign key (KvartiraId) references Kvartira(id)
);