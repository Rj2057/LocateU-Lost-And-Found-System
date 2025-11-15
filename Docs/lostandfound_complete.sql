DROP DATABASE IF EXISTS LostUDB;
CREATE DATABASE LostUDB;
USE LostUDB;

-- CREATE TABLES
CREATE TABLE student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    year_of_study INT CHECK (year_of_study BETWEEN 1 AND 5),
    password VARCHAR(255) NOT NULL
);

CREATE TABLE staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE lost_items (
    lost_item_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    category VARCHAR(50) NOT NULL,
    lost_date DATE NOT NULL,
    lost_loc VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Unresolved',
    item_name VARCHAR(100) NOT NULL,
    photo LONGBLOB NULL,
    description TEXT,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

CREATE TABLE found_items (
    f_i_id INT PRIMARY KEY AUTO_INCREMENT,
    report_student_id INT NULL,
    report_staff_id INT NULL,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    found_date DATE NOT NULL,
    found_loc VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Unclaimed',
    photo LONGBLOB NULL,
    FOREIGN KEY (report_student_id) REFERENCES student(student_id) ON DELETE SET NULL,
    FOREIGN KEY (report_staff_id) REFERENCES staff(staff_id) ON DELETE SET NULL
);

CREATE TABLE match_items (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    lost_item_id INT NOT NULL,
    f_i_id INT NOT NULL,
    match_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (lost_item_id) REFERENCES lost_items(lost_item_id) ON DELETE CASCADE,
    FOREIGN KEY (f_i_id) REFERENCES found_items(f_i_id) ON DELETE CASCADE
);

CREATE TABLE claims (
    claim_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT NOT NULL,
    student_id INT NOT NULL,
    proof_text TEXT NOT NULL,
    proof_file LONGBLOB NOT NULL,
    approval_status VARCHAR(20) DEFAULT 'Pending',
    verified_by_staff_id INT,
    FOREIGN KEY (match_id) REFERENCES match_items(match_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by_staff_id) REFERENCES staff(staff_id) ON DELETE SET NULL
);

CREATE TABLE notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Sent'
);


-- REQUIRED INSERTS
INSERT INTO student (name, email, phone_number, department, year_of_study, password)
VALUES 
('Rajat Bhat', 'rajat@example.com', '9999999991', 'CSE', 2, 'pwdhash1'),
('Alice Kumar', 'alice@example.com', '9999999992', 'ECE', 3, 'pwdhash2'),
('Bob Sharma', 'bob@example.com', '9999999993', 'CSE', 2, 'pwdhash3');

INSERT INTO staff (name, email, phone_number, role, department, password)
VALUES 
('S. Patel', 'patel@example.com', '8888888801', 'Security', 'Admin', 'pwdhashs1'),
('M. Singh', 'msingh@example.com', '8888888802', 'Helper', 'Admin', 'pwdhashs2');

INSERT INTO lost_items (student_id, category, lost_date, lost_loc, status, item_name, description)
VALUES
(1, 'Electronics', '2025-11-10', 'Library 1st Floor', 'Unresolved', 'Apple Watch Series 8', 'Silver watch'),
(2, 'Stationery', '2025-11-12', 'Block A Corridor', 'Unresolved', 'Calculator', 'Casio fx-991'),
(1, 'Electronics', '2025-11-11', 'Cafeteria', 'Unresolved', 'AirPods Pro', 'White case');

INSERT INTO found_items (report_student_id, report_staff_id, item_name, description, category, found_date, found_loc, status)
VALUES
(NULL, 1, 'Smartwatch', 'Found near library desk', 'Electronics', '2025-11-10', 'Library 1st Floor', 'Unclaimed'),
(3, NULL, 'Calculator', 'Found near Block A', 'Stationery', '2025-11-12', 'Block A Corridor', 'Unclaimed'),
(NULL, 2, 'Earbuds', 'White earbuds in case', 'Electronics', '2025-11-11', 'Cafeteria', 'Unclaimed');


-- FUNCTIONS
USE LostAndFoundDB;

DROP FUNCTION IF EXISTS CountLostItems;
DELIMITER //
CREATE FUNCTION CountLostItems(p_student_id INT)
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE lost_count INT;
    SELECT COUNT(*) INTO lost_count FROM lost_items WHERE student_id = p_student_id;
    RETURN lost_count;
END;
//
DELIMITER ;

DROP FUNCTION IF EXISTS GetClaimStatus;
DELIMITER //
CREATE FUNCTION GetClaimStatus(p_claim_id INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE status_val VARCHAR(20);
    SELECT approval_status INTO status_val FROM claims WHERE claim_id = p_claim_id;
    RETURN status_val;
END;
//
DELIMITER ;


-- PROCEDURES
DROP PROCEDURE IF EXISTS RegisterLostItem;
DELIMITER //
CREATE PROCEDURE RegisterLostItem(
    IN p_student_id INT, 
    IN p_category VARCHAR(50), 
    IN p_item_name VARCHAR(100), 
    IN p_description TEXT, 
    IN p_lost_date DATE, 
    IN p_lost_loc VARCHAR(100))
BEGIN
    INSERT INTO lost_items(student_id, category, item_name, description, lost_date, lost_loc, status) 
    VALUES (p_student_id, p_category, p_item_name, p_description, p_lost_date, p_lost_loc, 'Unresolved');
END;
//
DELIMITER ;

DROP PROCEDURE IF EXISTS MatchLostFound;
DELIMITER //
CREATE PROCEDURE MatchLostFound(IN p_lost_id INT, IN p_found_id INT)
BEGIN
    INSERT INTO match_items(lost_item_id, f_i_id, match_date, status) 
    VALUES (p_lost_id, p_found_id, CURDATE(), 'Pending');

    UPDATE lost_items SET status='Matched' WHERE lost_item_id=p_lost_id;
    UPDATE found_items SET status='Matched' WHERE f_i_id=p_found_id;
END;
//
DELIMITER ;


-- TRIGGERS
DROP TRIGGER IF EXISTS after_lost_item_insert;
DELIMITER //
CREATE TRIGGER after_lost_item_insert 
AFTER INSERT ON lost_items 
FOR EACH ROW 
BEGIN 
    INSERT INTO notifications (message, date, status) 
    VALUES (CONCAT('Lost item reported: ', NEW.item_name), CURDATE(), 'Unread'); 
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS after_claim_update_notify;
DELIMITER //
CREATE TRIGGER after_claim_update_notify 
AFTER UPDATE ON claims 
FOR EACH ROW 
BEGIN 
    IF NEW.verified_by_staff_id IS NOT NULL THEN 
        INSERT INTO notifications (message, date, status) 
        VALUES (CONCAT('Claim ', NEW.claim_id, ' ', NEW.approval_status), CURDATE(), 'Unread'); 
    END IF; 
END;
//
DELIMITER ;


-- NESTED QUERIES
SELECT s.student_id, s.name
FROM student s
WHERE (SELECT COUNT(*) FROM lost_items li WHERE li.student_id = s.student_id) > 1;

SELECT f.f_i_id, f.item_name, f.found_loc
FROM found_items f
WHERE f.report_student_id IN (
    SELECT s.student_id FROM student s WHERE s.department = 'CSE'
);

-- JOIN QUERIES
-- Inner join
SELECT c.claim_id, s.name AS student_name,
       li.item_name AS lost_item, fi.item_name AS found_item,
       c.approval_status
FROM claims c
JOIN student s ON c.student_id = s.student_id
JOIN match_items m ON c.match_id = m.match_id
JOIN lost_items li ON m.lost_item_id = li.lost_item_id
JOIN found_items fi ON m.f_i_id = fi.f_i_id
ORDER BY c.claim_id DESC
LIMIT 10;

-- Outer join
SELECT f.f_i_id, f.item_name, f.found_loc, m.match_id, m.status AS match_status
FROM found_items f
LEFT JOIN match_items m ON f.f_i_id = m.f_i_id
ORDER BY f.found_date DESC
LIMIT 20;


-- AGGREGATE QUERIES
SELECT category, COUNT(*) AS total_lost
FROM lost_items
GROUP BY category
ORDER BY total_lost DESC;

SELECT found_date, COUNT(*) AS found_count
FROM found_items
GROUP BY found_date
ORDER BY found_date DESC
LIMIT 30;

