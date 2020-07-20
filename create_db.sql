create user if not exists 'telegram_bot'@'localhost' IDENTIFIED BY 'powered_by_VINCIX';
create database if not exists Bot;
GRANT ALL PRIVILEGES ON Bot.* TO 'telegram_bot'@'localhost';

