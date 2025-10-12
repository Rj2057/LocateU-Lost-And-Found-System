DROP DATABASE IF EXISTS LostAndFoundDB;
CREATE DATABASE LostAndFoundDB;
USE LostAndFoundDB;
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