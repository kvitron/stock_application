CREATE DATABASE stock;
USE stock;

-- таблица Поставщики
CREATE TABLE vendors (
	id_vendor SMALLINT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
    address VARCHAR(50),
	CONSTRAINT PK_vendors__id_vendor PRIMARY KEY (id_vendor)
    );
    
-- таблица Отделы
CREATE TABLE departments (
	id_department TINYINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    CONSTRAINT PK_departments__id_departments PRIMARY KEY (id_department),
    CONSTRAINT UQ_departments__name UNIQUE (name) -- уникальное название отдела
	);
    
-- таблица Поставки
CREATE TABLE supplies (
	id_supply MEDIUMINT UNSIGNED AUTO_INCREMENT,
    id_vendor SMALLINT UNSIGNED NOT NULL,
    supply_date TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT PK_supplies__id_supply PRIMARY KEY (id_supply),
    CONSTRAINT FK_supplies__id_vendor FOREIGN KEY (id_vendor) REFERENCES vendors (id_vendor)
    );
    
-- таблица Покупки
CREATE TABLE purchases (
	id_purchase MEDIUMINT UNSIGNED AUTO_INCREMENT,
    purchase_date TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT PK_purchases__id_purchase PRIMARY KEY (id_purchase)
    );

-- таблица Товары
CREATE TABLE products (
	id_product INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    in_stock SMALLINT UNSIGNED NOT NULL,
    id_department TINYINT UNSIGNED,
    CONSTRAINT PK_products__id_product PRIMARY KEY (id_product),
    CONSTRAINT FK_products__id_department
		FOREIGN KEY (id_department)	REFERENCES departments (id_department)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	CONSTRAINT UQ_products__name UNIQUE (name), -- уникальное название товара
    CONSTRAINT CK_products__in_stock CHECK (in_stock >= 0)
    );

-- таблица Товары в поставке
CREATE TABLE products_in_supply (
	id_supply MEDIUMINT UNSIGNED NOT NULL,
    id_product INT UNSIGNED NOT NULL,
    quantity SMALLINT UNSIGNED NOT NULL,
    CONSTRAINT PK_products_in_supply PRIMARY KEY (id_supply, id_product),
    CONSTRAINT FK_products_in_supply__id_supply
		FOREIGN KEY (id_supply)	REFERENCES supplies (id_supply),
	CONSTRAINT FK_products_in_supply__id_product
		FOREIGN KEY (id_product) REFERENCES products (id_product),
	CONSTRAINT CK_products_in_supply__quantity CHECK (quantity >= 0)
	);

-- таблица Товары в покупке
CREATE TABLE products_in_purchase (
	id_purchase MEDIUMINT UNSIGNED NOT NULL,
    id_product INT UNSIGNED NOT NULL,
    quantity SMALLINT UNSIGNED NOT NULL,
    CONSTRAINT PK_products_in_purchase PRIMARY KEY (id_purchase, id_product),
    CONSTRAINT FK_products_in_purchase__id_purchase
		FOREIGN KEY (id_purchase) REFERENCES purchases (id_purchase),
	CONSTRAINT FK_products_in_purchase__id_product
		FOREIGN KEY (id_product) REFERENCES products (id_product),
	CONSTRAINT CK_products_in_purchase__quantity CHECK (quantity >= 0)
	);
    
-- Заполнение базы
INSERT INTO vendors (name, address) VALUES ('ОАО "Лучшая мебель"', 'Ул. Фурье 35а'); -- 1 поставщик
INSERT INTO vendors (name, address) VALUES ('ООО "Красное дерево"', 'Ул. Гмурмана 78'); -- 2 поставщик
INSERT INTO vendors (name, address) VALUES ('ОАО "Уют"', 'Пр. Эйлера 103'); -- 3 поставщик

INSERT INTO departments (name) VALUES ('Шкафы'); -- 1 отдел
INSERT INTO departments (name) VALUES ('Столы'); -- 2 отдел
INSERT INTO departments (name) VALUES ('Стулья'); -- 3 отдел
INSERT INTO departments (name) VALUES ('Диваны'); -- 4 отдел
INSERT INTO departments (name) VALUES ('Кресла'); -- 5 отдел
INSERT INTO departments (name) VALUES ('Кровати'); -- 6 отдел

INSERT INTO products (name, in_stock, id_department) VALUES ('Шкаф бежевый', 4, 1);
INSERT INTO products (name, in_stock, id_department) VALUES ('Шкаф коричневый', 1, 1);
INSERT INTO products (name, in_stock, id_department) VALUES ('Шкаф серый', 3, 1);
INSERT INTO products (name, in_stock, id_department) VALUES ('Шкаф белый', 2, 1);
INSERT INTO products (name, in_stock, id_department) VALUES ('Шкаф синий', 1, 1);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стол бежевый', 4, 2);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стол коричневый', 4, 2);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стол серый', 6, 2);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стол белый', 3, 2);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стул красный', 15, 3);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стул синий', 15, 3);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стул белый', 15, 3);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стул чёрный', 5, 3);
INSERT INTO products (name, in_stock, id_department) VALUES ('Стул коричневый', 5, 3);
INSERT INTO products (name, in_stock, id_department) VALUES ('Диван "Идеал"', 1, 4);
INSERT INTO products (name, in_stock, id_department) VALUES ('Диван "Простор"', 2, 4);
INSERT INTO products (name, in_stock, id_department) VALUES ('Диван "Отдых"', 1, 4);
INSERT INTO products (name, in_stock, id_department) VALUES ('Кресло "Отдых"', 3, 5);
INSERT INTO products (name, in_stock, id_department) VALUES ('Кресло "Домашнее"', 2, 5);
INSERT INTO products (name, in_stock, id_department) VALUES ('Кресло "Очаг"', 3, 5);
INSERT INTO products (name, in_stock, id_department) VALUES ('Кресло "Перина"', 2, 5);
INSERT INTO products (name, in_stock, id_department) VALUES ('Кровать "Идеал"', 2, 6);
INSERT INTO products (name, in_stock, id_department) VALUES ('Кровать "Перина"', 3, 6);
INSERT INTO products (name, in_stock, id_department) VALUES ('Кровать "Прнцесса на горошине"', 3, 6);

INSERT INTO supplies (id_vendor) VALUES (2); -- 1 поставка
INSERT INTO supplies (id_vendor) VALUES (1); -- 2 поставка
INSERT INTO supplies (id_vendor) VALUES (3); -- 3 поставка

INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 15, 1);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 16, 2);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 17, 1);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 18, 3);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 19, 2);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 20, 3);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 21, 2);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 22, 2);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 23, 3);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (1, 24, 3);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (2, 1, 4);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (2, 2, 1);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (2, 3, 3);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (2, 4, 2);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (2, 5, 1);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 6, 4);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 7, 4);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 8, 6);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 9, 3);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 10, 15);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 11, 15);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 12, 15);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 13, 5);
INSERT INTO products_in_supply (id_supply, id_product, quantity) VALUES (3, 14, 5);

/*
INSERT INTO products_in_purchase (id_purchase, id_product, quantity) VALUES (1, 9, 1);
INSERT INTO products_in_purchase (id_purchase, id_product, quantity) VALUES (1, 12, 2);
INSERT INTO products_in_purchase (id_purchase, id_product, quantity) VALUES (2, 17, 1);
INSERT INTO products_in_purchase (id_purchase, id_product, quantity) VALUES (3, 2, 1);
INSERT INTO products_in_purchase (id_purchase, id_product, quantity) VALUES (3, 23, 1);
*/

-- Триггер увеличения количества товара на складе при поставке
DROP TRIGGER IF EXISTS `stock`.`products_in_supply_AFTER_INSERT`;
DELIMITER $$
USE `stock`$$
CREATE TRIGGER `stock`.`products_in_supply_AFTER_INSERT` AFTER INSERT ON `products_in_supply` FOR EACH ROW
	BEGIN
	UPDATE products SET in_stock = in_stock + NEW.quantity WHERE products.id_product = NEW.id_product;
	END$$
DELIMITER ;

-- Триггер уменьшения количества товара на складе при покупке
DROP TRIGGER IF EXISTS `stock`.`products_in_purchase_AFTER_INSERT`;
DELIMITER $$
USE `stock`$$
CREATE TRIGGER `stock`.`products_in_purchase_AFTER_INSERT` AFTER INSERT ON `products_in_purchase` FOR EACH ROW
BEGIN
UPDATE products SET in_stock = in_stock - NEW.quantity WHERE products.id_product = NEW.id_product;
END$$
DELIMITER ;
    
/*
- придумать наиболее часто встречающиеся запросы:
		- по названию товара <name> вывести всю информацию о нем
        - оформить покупку
        - оформить поставку
        - добавить поставщика
        - добавить вид товара
        - добавить/удалить отдел
        - просмотр проданного за период времени по каждому отделу и по складу в целом
*/

-- создание новых пользователей
/*
CREATE USER 'stock_admin'@'%' IDENTIFIED BY '1001'; -- '%' доступен со всех хостов
GRANT SELECT,UPDATE,INSERT,DELETE ON stock . * TO 'stock_admin'@'%';
*/
-- REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'administrator'@'%';
-- DROP USER 'administrator'@'%';

-- просмотр всех пользователей
-- SELECT User,Host FROM mysql.user;
