CREATE TABLE urls (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(64) NOT NULL,
    created_at date default current_date
);
