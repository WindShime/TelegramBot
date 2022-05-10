create table budget(
    codename varchar(255) primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

create table income(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "продукты", true, "еда"),
    ("subscriptions", "подписки", false, "подписка"),
    ("internet", "интернет", false, "инет"),
    ("phone", "телефон", false, "связь"),
    ("transport", "общ. транспорт", false, "транспорт"),
    ("taxi", "такси", false, "убер"),
    ("cafe", "кафе", true, "ресторан"),
    ("income", "доход", true, "зарплата"),
    ("other", "прочее", true, "другое");

insert into budget(codename, daily_limit) values ('base', 1000);
