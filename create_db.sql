create user if not exists 'telegram_bot'@'localhost' IDENTIFIED BY 'powered_by_VINCIX';
create database if not exists Bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON Bot.* TO 'telegram_bot'@'localhost';



