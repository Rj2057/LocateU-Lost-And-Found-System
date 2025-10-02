DROP DATABASE IF EXISTS LostAndFoundDB;
CREATE DATABASE LostAndFoundDB;
USE LostAndFoundDB;


CREATE TABLE Student (
    Student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    Phone_no VARCHAR(15) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    Year_Study INT CHECK (Year_Study BETWEEN 1 AND 5),
    password VARCHAR(100) NOT NULL
);


CREATE TABLE Staff (
    Staff_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    Phone_no VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    Role VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL
);


CREATE TABLE Lost_items (
    Lost_item_id INT PRIMARY KEY AUTO_INCREMENT,
    Student_id INT,
    Category VARCHAR(50) NOT NULL,
    Lost_date DATE NOT NULL,
    Lost_loc VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Unresolved',
    Item_name VARCHAR(100) NOT NULL,
    photo BLOB NULL,
    description TEXT,
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id)
);


CREATE TABLE Found_items (
    F_I_id INT PRIMARY KEY AUTO_INCREMENT,
    Report_student_id INT NULL,
    Report_staff_id INT NULL,
    Item_name VARCHAR(100) NOT NULL,
    description TEXT,
    Category VARCHAR(50) NOT NULL,
    Found_date DATE NOT NULL,
    Found_loc VARCHAR(100) NOT NULL,
    Status VARCHAR(20) DEFAULT 'Unclaimed',
    photo BLOB NULL,
    FOREIGN KEY (Report_student_id) REFERENCES Student(Student_id),
    FOREIGN KEY (Report_staff_id) REFERENCES Staff(Staff_id)
);


CREATE TABLE Match_items (
    Match_id INT PRIMARY KEY AUTO_INCREMENT,
    Lost_item_id INT NOT NULL,
    F_I_id INT NOT NULL,
    Match_date DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (Lost_item_id) REFERENCES Lost_items(Lost_item_id),
    FOREIGN KEY (F_I_id) REFERENCES Found_items(F_I_id)
);


CREATE TABLE Claims (
    Claim_id INT PRIMARY KEY AUTO_INCREMENT,
    Match_id INT NOT NULL,
    Student_id INT NOT NULL,
    Proof_submitted TEXT NOT NULL,
    Approval_status VARCHAR(20) DEFAULT 'Pending',
    Verified_by_Staff_id INT,
    FOREIGN KEY (Match_id) REFERENCES Match_items(Match_id),
    FOREIGN KEY (Student_id) REFERENCES Student(Student_id),
    FOREIGN KEY (Verified_by_Staff_id) REFERENCES Staff(Staff_id)
);


CREATE TABLE Notifications (
    Notification_id INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Unread'
);


INSERT INTO Student (name, email, Phone_no, department, Year_Study, password)
VALUES 
('Alice Kumar', 'alice@pes.edu', '9876543210', 'CSE', 2, 'alice123'),
('Rahul Mehta', 'rahul@pes.edu', '9876500001', 'ECE', 3, 'rahul123'),
('Sneha Rao', 'sneha@pes.edu', '9876500002', 'ME', 1, 'sneha123');


INSERT INTO Staff (name, Phone_no, email, Role, department)
VALUES
('Prof. Shankar', '9876500003', 'shankar@pes.edu', 'Admin', 'CSE'),
('Dr. Kavita', '9876500004', 'kavita@pes.edu', 'Verifier', 'ECE');


INSERT INTO Lost_items (Student_id, Category, Lost_date, Lost_loc, status, Item_name, photo, description)
VALUES
(1, 'Electronics', '2025-09-01', 'Library', 'Unresolved', 'Calculator', 'dummy_image_1', 'Casio fx-991EX black scientific calculator'),
(2, 'Stationery', '2025-09-10', 'Canteen', 'Unresolved', 'Notebook', 'dummy_image_2', 'Red spiral notebook');

INSERT INTO Found_items (Report_student_id, Report_staff_id, Item_name, description, Category, Found_date, Found_loc, Status, photo)
VALUES
(1, NULL, 'Calculator', 'Black Casio calculator found near library', 'Electronics', '2025-09-02', 'Library Entrance', 'Unclaimed', 'dummy_image_3'),
(NULL, 2, 'Notebook', 'Spiral notebook found on table', 'Stationery', '2025-09-10', 'Canteen', 'Unclaimed', 'dummy_image_4');


INSERT INTO Match_items (Lost_item_id, F_I_id, Match_date, Status)
VALUES
(1, 1, '2025-09-03', 'Pending'),
(2, 2, '2025-09-11', 'Pending');


INSERT INTO Claims (Match_id, Student_id, Proof_submitted, Approval_status, Verified_by_Staff_id)
VALUES
(1, 1, 'Bill copy of calculator purchase', 'Pending', 1),
(2, 2, 'Notebook with handwritten notes inside', 'Pending', 2);

INSERT INTO Notifications (message, date, status)
VALUES
('Lost item Calculator reported by Alice', '2025-09-01', 'Unread'),
('Found item Notebook reported by Staff Kavita', '2025-09-10', 'Unread');
