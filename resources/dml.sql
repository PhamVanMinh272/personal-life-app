-- Name is unique to avoid duplicate
INSERT INTO category (id, name) VALUES (1, "Furniture");
INSERT INTO category (id, name) VALUES (2, "Electronics");
INSERT INTO category (id, name) VALUES (3, "Clothing");
INSERT INTO category (id, name) VALUES (4, "Books");
INSERT INTO category (id, name) VALUES (5, "Other");

INSERT INTO product (id, name, category_id, stock_quantity) VALUES (1, "Chair", 1, 50);
INSERT INTO product (id, name, category_id, stock_quantity) VALUES (2, "Table", 1, 20);
