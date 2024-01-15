CREATE TABLE urls (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(64) NOT NULL,
    created_at date default current_date
);

CREATE TABLE url_checks (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id int NOT NULL,
    status_code smallint,
    h1 varchar(128),
    title varchar(256),
    description text,
    created_at date default current_date
);
