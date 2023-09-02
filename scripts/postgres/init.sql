CREATE TABLE users
(
    id_tg bigint PRIMARY KEY
);



CREATE TABLE levels
(
    id_level   bigint PRIMARY KEY,
    req_sum    bigint,
    name_level varchar
);

CREATE TABLE user_data
(

    id_user                bigint unique,
    name              varchar(255),
    sec_name          varchar(255),
    last_name         varchar(20),
    phone_number      bigint,
    date_registration timestamp,
    status            boolean NOT NULL,
    level bigint,
    FOREIGN KEY (id_user) REFERENCES users (id_tg),
    FOREIGN KEY (level) REFERENCES levels(id_level)
);

CREATE TABLE donation (
        id_donat  serial PRIMARY KEY,
        id_user bigint,
        sum bigint,
        date_donation timestamp,
        FOREIGN KEY (id_user) REFERENCES users(id_tg)

);


CREATE TABLE discounts(
    id_discount serial PRIMARY KEY,
    company_name varchar,
    description varchar,
    promo varchar,
    discount varchar,
    date_start timestamp,
    date_end timestamp,
    req_level bigint,
    FOREIGN KEY (req_level) REFERENCES levels(id_level)
);
