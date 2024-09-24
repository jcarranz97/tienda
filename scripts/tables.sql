create database bagsiuesei;
use bagsiuesei;
SHOW TABLES;

CREATE TABLE product_availability (
    id_availability INT AUTO_INCREMENT PRIMARY KEY,
    availability_status VARCHAR(50) NOT NULL
);


CREATE TABLE sellers(
	id_seller INT AUTO_INCREMENT PRIMARY KEY,
	seller_name VARCHAR(20)
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE shipping_vendors (
    id_vendor INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL
);

CREATE TABLE shipping_statuses (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE shipping_groups (
    id_shipping_group INT AUTO_INCREMENT PRIMARY KEY,
    shipping_group_name VARCHAR(255) NOT NULL,
    id_vendor INT NOT NULL,
    id_status INT NOT NULL,
    shipping_cost DECIMAL(10, 2) NOT NULL,
    dollar_price DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	notes TEXT,
    FOREIGN KEY (id_vendor) REFERENCES shipping_vendors(id_vendor),
    FOREIGN KEY (id_status) REFERENCES shipping_statuses(id_status)
);

CREATE TABLE locations (
    id_location INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL
);

CREATE TABLE products (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    shipping_label VARCHAR(255),
    purchase_price DECIMAL(10, 2) NOT NULL,
    purchase_price_mxn DECIMAL(10, 2) NOT NULL,
    selling_price DECIMAL(10, 2) NOT NULL,
    product_availability_id INT NOT NULL,
    current_location_id INT NOT NULL,
    seller_id INT NOT NULL,
    shipping_group_id INT NOT NULL,
    FOREIGN KEY (product_availability_id) REFERENCES product_availability(id_availability),
    FOREIGN KEY (seller_id) REFERENCES sellers(id_seller),
    FOREIGN KEY (shipping_group_id) REFERENCES shipping_groups(id_shipping_group),
    FOREIGN KEY (current_location_id) REFERENCES locations(id_location)
);


-- product availabilities
INSERT INTO product_availability (availability_status) 
VALUES 
('available'),
('not available'),
('in transit'),
('reserved');

INSERT INTO sellers (seller_name) 
VALUES 
('oriana'),
('gris'),
('montse'),
('aylin'),
('nayeli');

INSERT INTO shipping_vendors (vendor_name) 
VALUES 
('envios cuevas');

INSERT INTO shipping_statuses (status_name, description)
VALUES 
('pending', 'Shipment is created but not yet processed.'),
('in transit', 'Shipment is currently on its way to the destination.'),
('delivered', 'Shipment has been successfully delivered.'),
('returned', 'Shipment has been returned to the sender.'),
('cancelled', 'Shipment has been cancelled.'),
('exception', 'There is a delay or issue with the shipment.');

INSERT INTO shipping_groups (shipping_group_name, id_vendor, id_status, shipping_cost, dollar_price)
VALUES
("ventas1-mayo", 1, 2, 100, 16.60);

INSERT INTO locations (location_name)
VALUES
("casa de oriana");

CREATE TABLE products (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    shipping_label VARCHAR(255),
    purchase_price DECIMAL(10, 2) NOT NULL,
    purchase_price_mxn DECIMAL(10, 2) NOT NULL,
    selling_price DECIMAL(10, 2) NOT NULL,
    product_availability_id INT NOT NULL,
    current_location_id INT NOT NULL,
    seller_id INT NOT NULL,
    shipping_group_id INT NOT NULL,
    FOREIGN KEY (product_availability_id) REFERENCES product_availability(id_availability),
    FOREIGN KEY (seller_id) REFERENCES sellers(id_seller),
    FOREIGN KEY (shipping_group_id) REFERENCES shipping_groups(id_shipping_group),
    FOREIGN KEY (current_location_id) REFERENCES locations(id_location)
);

INSERT INTO products (description, shipping_label, purchase_price, purchase_price_mxn, selling_price, product_availability_id, current_location_id, seller_id, shipping_group_id)
VALUES
("Bolsa1", "Valeria", 40.00, 691.20, 1200.00, 2, 1, 1, 1),
("Bolsa2", "Gabriela", 40.00, 691.20, 1200.00, 2, 1, 1, 1),
("Bolsa3", "Ximena", 40.00, 691.20, 1200.00, 2, 1, 1, 1);
