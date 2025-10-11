-- (Provided functions / procedures / triggers - included for reference)
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
DROP PROCEDURE IF EXISTS RegisterLostItem;
DELIMITER //
CREATE PROCEDURE RegisterLostItem(IN p_student_id INT, IN p_category VARCHAR(50), IN p_item_name VARCHAR(100), IN p_description TEXT, IN p_lost_date DATE, IN p_lost_loc VARCHAR(100))
BEGIN
    INSERT INTO lost_items(student_id, category, item_name, description, lost_date, lost_loc, status) VALUES (p_student_id, p_category, p_item_name, p_description, p_lost_date, p_lost_loc, 'Unresolved');
END;
//
DELIMITER ;
DROP PROCEDURE IF EXISTS MatchLostFound;
DELIMITER //
CREATE PROCEDURE MatchLostFound(IN p_lost_id INT, IN p_found_id INT)
BEGIN
    INSERT INTO match_items(lost_item_id, f_i_id, match_date, status) VALUES (p_lost_id, p_found_id, CURDATE(), 'Pending');
    UPDATE lost_items SET status='Matched' WHERE lost_item_id=p_lost_id;
    UPDATE found_items SET status='Matched' WHERE f_i_id=p_found_id;
END;
//
DELIMITER ;
DROP TRIGGER IF EXISTS after_lost_item_insert;
DELIMITER //
CREATE TRIGGER after_lost_item_insert AFTER INSERT ON lost_items FOR EACH ROW BEGIN INSERT INTO notifications (message, date, status) VALUES (CONCAT('Lost item reported: ', NEW.item_name), CURDATE(), 'Unread'); END;
//
DELIMITER ;
DROP TRIGGER IF EXISTS after_claim_update_notify;
DELIMITER //
CREATE TRIGGER after_claim_update_notify AFTER UPDATE ON claims FOR EACH ROW BEGIN IF NEW.verified_by_staff_id IS NOT NULL THEN INSERT INTO notifications (message, date, status) VALUES (CONCAT('Claim ', NEW.claim_id, ' ', NEW.approval_status), CURDATE(), 'Unread'); END IF; END;
//
DELIMITER ;
