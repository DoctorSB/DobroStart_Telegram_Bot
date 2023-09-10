CREATE TABLE levels
(
    id_level   bigint PRIMARY KEY,
    req_sum    bigint,
    name_level varchar
);

CREATE TABLE users_data
(

    id_tg             bigint unique,
    name              varchar(255),
    sec_name          varchar(255),
    last_name         varchar(255),
    phone_number      bigint,
    email             varchar(255),
    date_registration timestamp,
    sum_donation BIGINT default 0,
    status            boolean NOT NULL,
    level             bigint,
    FOREIGN KEY (level) REFERENCES levels (id_level)
);

CREATE TABLE donation
(
    id_donat      serial PRIMARY KEY,
    id_user       bigint,
    sum           bigint,
    date_donation timestamp,
    FOREIGN KEY (id_user) REFERENCES users_data (id_tg)

);


CREATE TABLE discounts
(
    id_discount  serial PRIMARY KEY,
    company_name varchar,
    description  varchar,
    promo        varchar,
    discount     varchar,
    date_start   timestamp,
    date_end     timestamp,
    req_level    bigint,
    FOREIGN KEY (req_level) REFERENCES levels (id_level)
);


INSERT INTO levels (id_level, req_sum, name_level)
VALUES (0, 0, 'beginner'),
       (1, 1000, 'beginner+'),
       (2, 2000, 'intermediate'),
       (3, 3000, 'intermediate+');


INSERT INTO discounts (company_name, description, promo, discount, date_start, date_end, req_level)
VALUES
  ('company1', 'description1', 'promo1', 10, '2023-09-01 00:00:00', '2023-09-30 23:59:59', 1),
  ('company2', 'description2', 'promo2', 15, '2023-09-01 00:00:00', '2023-09-30 23:59:59', 2),
  ('company3', 'description3', 'promo3', 20, '2023-09-01 00:00:00', '2023-09-30 23:59:59', 3),
  ('company4', 'description4', 'promo4', 25, '2023-09-01 00:00:00', '2023-09-30 23:59:59', 1),
  ('company5', 'description5', 'promo5', 30, '2023-09-01 00:00:00', '2023-09-30 23:59:59', 2);


INSERT INTO users_data (id_tg, name, sec_name, last_name, phone_number, email, date_registration, status, level)
VALUES
  (123456789, 'John', 'Doe', 'Smith', '1234567890', 'john.doe@example.com', '2023-09-01 12:34:56', true, 1),
  (987654321, 'Jane', 'Smith', 'Doe', '0987654321', 'jane.smith@example.com', '2023-09-02 09:00:00', false, 2),
  (456789123, 'Alice', 'Johnson', 'Brown', '9876543210', 'alice.johnson@example.com', '2023-09-03 15:30:00', true, 3);


CREATE OR REPLACE FUNCTION get_discounts_by_user_id(user_id bigint)
  RETURNS TABLE (company_name varchar, description varchar, promo varchar, discount varchar, lvl bigint)
  AS $$
  BEGIN
    RETURN QUERY
    SELECT d.company_name, d.description, d.promo, d.discount, d.req_level
    FROM discounts d
    WHERE d.req_level <= (SELECT level FROM users_data WHERE id_tg = user_id)
    order by d.req_level desc ;
  END;
  $$
  LANGUAGE plpgsql;