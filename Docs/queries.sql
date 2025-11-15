-- Nested Query
SELECT s.student_id, s.name
FROM student s
WHERE (SELECT COUNT(*) FROM lost_items li WHERE li.student_id = s.student_id) > 1;

SELECT f.f_i_id, f.item_name, f.found_loc
FROM found_items f
WHERE f.report_student_id IN (
    SELECT s.student_id FROM student s WHERE s.department = 'CSE'
);

-- Join 
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

-- Aggregate query
SELECT category, COUNT(*) AS total_lost
FROM lost_items
GROUP BY category
ORDER BY total_lost DESC;

SELECT found_date, COUNT(*) AS found_count
FROM found_items
GROUP BY found_date
ORDER BY found_date DESC
LIMIT 30;




