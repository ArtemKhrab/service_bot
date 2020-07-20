insert into bot.city (name) values ('Київ');
insert into bot.city (name) values ('Львів');
insert into bot.city (name) values ('Одеса');
insert into bot.city (name) values ('Харків');
insert into bot.city (name) values ('Дніпро');
insert into bot.city (name) values ('Запоріжжя');
insert into bot.city (name) values ('Кривий Ріг');
insert into bot.city (name) values ('Миколаїв');
insert into bot.city (name) values ('Вінниця');
insert into bot.placement (name, latitude, longitude, address, city_id) values ('Blossom', 1, 1, 'вул. Шимановського 1/2', 1);
insert into bot.service_segment (name)values ('Брови, вії');
insert into bot.service_segment  (name)values ('Нігтьовий сервіс');
insert into bot.service_segment  (name)values ('Перукарські послуги');



-- set default-character-set=utf8mb4;
-- SET names utf8mb4;
-- show variables like '%char%';
-- SET NAMES 'utf8mb4'; SET character_set_connection='utf8mb4';

-- ALTER DATABASE Bot CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
-- ALTER DATABASE bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ALTER TABLE bot.city CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- ALTER TABLE bot.city MODIFY name TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- set character_set_client = utf8mb4;
-- set character_set_system = utf8mb4;
-- set character_set_client_handshake = FALSE;
-- set character_set_server = utf8mb4;
-- set collation_server = utf8mb4_unicode_ci;