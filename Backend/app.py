from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from database import get_db_connection, execute_query, call_procedure, call_function
import io
import base64
from datetime import datetime
from difflib import SequenceMatcher

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.secret_key = Config.APP_SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


# HELPER FUNCTIONS

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_notification(message, notif_type="Info"):
    """Insert a new system notification"""
    query = """
        INSERT INTO notifications (message, notif_type, status, date)
        VALUES (%s, %s, 'Unread', NOW())
    """
    execute_query(query, (message, notif_type))


# HOME & AUTH ROUTES

@app.route('/')
def index():
    """Landing page with login/register options"""
    return render_template('index.html')

@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    """Student registration"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        year = request.form['year']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        query = """
            INSERT INTO student (name, email, phone_number, department, year_of_study, password) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = execute_query(query, (name, email, phone, department, year, hashed_password))
        
        if result:
            return jsonify({'success': True, 'message': 'Registration successful'})
        else:
            return jsonify({'success': False, 'message': 'Registration failed. Email or phone may already exist.'})
    
    return render_template('index.html')


@app.route('/student/login', methods=['POST'])
def student_login():
    """Student login"""
    email = request.form['email']
    password = request.form['password']
    
    query = "SELECT * FROM student WHERE email = %s"
    user = execute_query(query, (email,), fetch=True, fetchone=True)
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['student_id']
        session['user_type'] = 'student'
        session['user_name'] = user['name']
        session['user_email'] = user['email']  # Store email in session
        return jsonify({'success': True, 'redirect': url_for('student_dashboard')})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/staff/register', methods=['GET', 'POST'])
def staff_register():
    """Staff registration"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        department = request.form['department']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        query = """INSERT INTO staff (name, email, phone_number, role, department, password) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        result = execute_query(query, (name, email, phone, role, department, hashed_password))
        
        if result:
            return jsonify({'success': True, 'message': 'Registration successful'})
        else:
            return jsonify({'success': False, 'message': 'Registration failed'})
    
    return render_template('index.html')

@app.route('/staff/login', methods=['POST'])
def staff_login():
    """Staff login"""
    email = request.form['email']
    password = request.form['password']
    
    query = "SELECT * FROM staff WHERE email = %s"
    user = execute_query(query, (email,), fetch=True, fetchone=True)
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['staff_id']
        session['user_type'] = 'staff'
        session['user_name'] = user['name']
        return jsonify({'success': True, 'redirect': url_for('staff_dashboard')})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))


# STUDENT DASHBOARD ROUTES

@app.route('/student/dashboard')
def student_dashboard():
    """Student dashboard"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('index'))
    
    # Use CountLostItems function
    lost_count = call_function(f"SELECT CountLostItems({session['user_id']})")
    
    # Get student email for filtering notifications
    student_query = "SELECT email FROM student WHERE student_id = %s"
    student = execute_query(student_query, (session['user_id'],), fetch=True, fetchone=True)
    student_email = student['email'] if student else None
    
    # Get user-specific notifications (messages starting with [email])
    if student_email:
        notif_query = """
            SELECT * FROM notifications 
            WHERE message LIKE %s OR message NOT LIKE '[%'
            ORDER BY date DESC LIMIT 10
        """
        notifications = execute_query(notif_query, (f"[{student_email}]%",), fetch=True) or []
        
        # Clean up the email prefix from notification messages for display
        for notif in notifications:
            if notif['message'].startswith(f"[{student_email}]"):
                notif['message'] = notif['message'].replace(f"[{student_email}] ", "")
    else:
        notifications = []
    
    # Get student's lost items
    query = """SELECT * FROM lost_items WHERE student_id = %s ORDER BY lost_date DESC"""
    lost_items = execute_query(query, (session['user_id'],), fetch=True) or []
    
    return render_template('student_dashboard.html', 
                         user_name=session['user_name'],
                         lost_count=lost_count or 0,
                         notifications=notifications,
                         lost_items=lost_items)


@app.route('/student/report-lost', methods=['GET', 'POST'])
def report_lost():
    """Report lost item"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        category = request.form['category']
        item_name = request.form['item_name']
        description = request.form['description']
        lost_date = request.form['lost_date']
        lost_loc = request.form['lost_loc']
        
        # Use RegisterLostItem stored procedure
        success = call_procedure('RegisterLostItem', (
            session['user_id'], category, item_name, 
            description, lost_date, lost_loc
        ))
        
        if success and 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                photo_data = photo.read()
                
                # Get the last inserted lost_item_id
                query = """SELECT lost_item_id FROM lost_items 
                          WHERE student_id = %s ORDER BY lost_item_id DESC LIMIT 1"""
                result = execute_query(query, (session['user_id'],), fetch=True, fetchone=True)
                
                if result:
                    # Update photo using BINARY format
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    update_query = "UPDATE lost_items SET photo = %s WHERE lost_item_id = %s"
                    cursor.execute(update_query, (photo_data, result['lost_item_id']))
                    conn.commit()
                    cursor.close()
                    conn.close()
        
        if success:
            return jsonify({'success': True, 'message': 'Lost item reported successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to report item'})
    
    return render_template('report_lost.html', user_name=session['user_name'])

@app.route('/student/report-found', methods=['GET', 'POST'])
def report_found():
    """Report found item"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        category = request.form['category']
        item_name = request.form['item_name']
        description = request.form['description']
        found_date = request.form['found_date']
        found_loc = request.form['found_loc']
        
        # Insert found item
        query = """INSERT INTO found_items (report_student_id, category, item_name, 
                   description, found_date, found_loc, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, 'Unclaimed')"""
        result = execute_query(query, (session['user_id'], category, item_name, 
                                      description, found_date, found_loc))
        

        # store photo against that id.
        if result and 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                photo_data = photo.read()
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE found_items SET photo = %s WHERE f_i_id = %s", (photo_data, result))
                conn.commit()
                cursor.close()
                conn.close()
        
        # Notify staff (notifications table is global in your schema)
        notif_msg = f"New found item reported by {session['user_name']}: {item_name} at {found_loc} on {found_date}"
        execute_query("INSERT INTO notifications (message, date, status) VALUES (%s, CURDATE(), 'Unread')", (notif_msg,))
        
        if result:
            return jsonify({'success': True, 'message': 'Found item reported successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to report item'})
    
    return render_template('report_found.html', user_name=session['user_name'])


@app.route('/student/claim-item', methods=['GET', 'POST'])
def claim_item():
    """Claim an item"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        found_id = request.form['found_id']
        proof_text = request.form.get('proof_text', '')
        proof_file = request.files.get('proof_file')
        
        # Get latest unresolved lost item of student
        lost_item = execute_query(
            "SELECT lost_item_id, item_name FROM lost_items WHERE student_id = %s AND status IN ('Unresolved', 'Matched') ORDER BY lost_date DESC LIMIT 1",
            (session['user_id'],),
            fetch=True, fetchone=True
        )
        if not lost_item:
            return jsonify({'success': False, 'message': 'No unresolved lost item found'})

        # Ensure the found item exists and is unclaimed OR matched (pending claim)
        found_item = execute_query(
            "SELECT f_i_id, item_name, status FROM found_items WHERE f_i_id = %s", 
            (found_id,), fetch=True, fetchone=True
        )
        if not found_item or found_item.get('status') not in ['Unclaimed', 'Matched']:
            return jsonify({'success': False, 'message': 'Selected found item is not available for claiming'})

        # Check if match already exists
        existing_match = execute_query(
            "SELECT match_id FROM match_items WHERE lost_item_id = %s AND f_i_id = %s ORDER BY match_id DESC LIMIT 1",
            (lost_item['lost_item_id'], found_id), fetch=True, fetchone=True
        )
        
        if existing_match:
            # Match already exists, use it
            match_id = existing_match['match_id']
        else:
            # Create new match using stored procedure
            call_procedure('MatchLostFound', (lost_item['lost_item_id'], found_id))
            
            # Get new match_id
            match_row = execute_query(
                "SELECT match_id FROM match_items WHERE lost_item_id = %s AND f_i_id = %s ORDER BY match_id DESC LIMIT 1",
                (lost_item['lost_item_id'], found_id), fetch=True, fetchone=True
            )
            if not match_row:
                return jsonify({'success': False, 'message': 'Match creation failed'})
            
            match_id = match_row['match_id']
            
            # Global notification for match creation
            notif_msg = f"New match created: Lost Item '{lost_item['item_name']}' ↔ Found Item '{found_item['item_name']}'"
            create_notification(notif_msg)

        # Check if claim already exists for this match
        existing_claim = execute_query(
            "SELECT claim_id FROM claims WHERE match_id = %s AND student_id = %s",
            (match_id, session['user_id']), fetch=True, fetchone=True
        )
        
        if existing_claim:
            return jsonify({'success': False, 'message': 'You have already submitted a claim for this item'})

        # Insert claim in pending state
        if proof_file:
            proof_data = proof_file.read()
            if not proof_data:
                proof_data = b''
        else:
            proof_data = b''

        execute_query(
            "INSERT INTO claims (match_id, student_id, proof_text, proof_file, approval_status, verified_by_staff_id) VALUES (%s, %s, %s, %s, 'Pending', NULL)",
            (match_id, session['user_id'], proof_text, proof_data)
        )

        # Notify the student about claim submission
        student_email_query = "SELECT email FROM student WHERE student_id = %s"
        student = execute_query(student_email_query, (session['user_id'],), fetch=True, fetchone=True)
        if student:
            claim_notif = f"📋 Your claim for '{found_item.get('item_name')}' has been submitted and is pending staff review."
            execute_query(
                "INSERT INTO notifications (message, date, status) VALUES (%s, CURDATE(), 'Unread')",
                (f"[{student['email']}] {claim_notif}",)
            )

        # Notify staff that a claim was submitted
        notif_msg = f"New claim submitted by {session['user_name']} for found item '{found_item.get('item_name')}' (found_id={found_id})"
        execute_query("INSERT INTO notifications (message, date, status) VALUES (%s, CURDATE(), 'Unread')", (notif_msg,))

        return jsonify({'success': True, 'message': 'Claim submitted successfully; staff will review it'})
    
    # GET: Show items that are Unclaimed OR have a Pending match for this student
    found_items = execute_query("""
        SELECT DISTINCT f.*, 
               CASE WHEN f.report_student_id IS NOT NULL THEN s.name ELSE st.name END AS reporter_name,
               m.match_id,
               m.status as match_status
        FROM found_items f
        LEFT JOIN student s ON f.report_student_id = s.student_id
        LEFT JOIN staff st ON f.report_staff_id = st.staff_id
        LEFT JOIN match_items m ON f.f_i_id = m.f_i_id AND m.status = 'Pending'
        LEFT JOIN lost_items li ON m.lost_item_id = li.lost_item_id AND li.student_id = %s
        WHERE (f.status = 'Unclaimed' OR (f.status = 'Matched' AND m.match_id IS NOT NULL))
        AND NOT EXISTS (
            SELECT 1 FROM claims c 
            WHERE c.match_id = m.match_id 
            AND c.student_id = %s
        )
        ORDER BY f.found_date DESC
    """, (session['user_id'], session['user_id']), fetch=True) or []

    return render_template('claim_item.html', user_name=session['user_name'], found_items=found_items)



# STAFF DASHBOARD ROUTES

@app.route('/staff/dashboard')
def staff_dashboard():
    """Staff dashboard"""
    if 'user_id' not in session or session.get('user_type') != 'staff':
        return redirect(url_for('index'))
    
    # Get statistics
    stats_query = """SELECT 
        (SELECT COUNT(*) FROM claims WHERE approval_status = 'Pending') as pending_claims,
        (SELECT COUNT(*) FROM lost_items WHERE status = 'Unresolved') as unresolved_lost,
        (SELECT COUNT(*) FROM found_items WHERE status = 'Unclaimed') as unclaimed_found,
        (SELECT COUNT(*) FROM match_items WHERE status = 'Pending') as pending_matches"""
    stats = execute_query(stats_query, fetch=True, fetchone=True)
    
    # Get notifications (staff sees global notifications)
    query = """SELECT * FROM notifications WHERE message NOT LIKE '[%' OR message LIKE '[staff%' ORDER BY date DESC LIMIT 10"""
    notifications = execute_query(query, fetch=True) or []
    
    return render_template('staff_dashboard.html', 
                         user_name=session['user_name'],
                         stats=stats,
                         notifications=notifications)

@app.route('/staff/claims', methods=['GET'])
def staff_claims():
    """View all claims"""
    if 'user_id' not in session or session.get('user_type') != 'staff':
        return redirect(url_for('index'))
    

    query = """
        SELECT 
            c.claim_id,
            c.proof_text,
            c.approval_status,
            s.name AS student_name,
            s.email AS student_email,
            li.item_name AS lost_item_name,
            li.category AS lost_category,
            fi.item_name AS found_item_name,
            fi.found_loc,
            DATE_FORMAT(m.match_date, '%Y-%m-%d') AS match_date,
            m.status AS match_status,
            LENGTH(c.proof_file) AS proof_size
        FROM claims c
        JOIN student s ON c.student_id = s.student_id
        JOIN match_items m ON c.match_id = m.match_id
        JOIN lost_items li ON m.lost_item_id = li.lost_item_id
        JOIN found_items fi ON m.f_i_id = fi.f_i_id
        ORDER BY m.match_date DESC
    """
    claims = execute_query(query, fetch=True) or []

    # Convert proof_size to boolean flag for template (proof exists if proof_size > 0)
    for row in claims:
        row['has_proof'] = bool(row.get('proof_size', 0))

    return render_template('staff_claims.html', 
                           user_name=session['user_name'],
                           claims=claims)

@app.route('/staff/verify-claim/<int:claim_id>/<action>', methods=['POST'])
def verify_claim(claim_id, action):
    """Approve or reject claim (triggers DB notification via trigger after update)"""
    if 'user_id' not in session or session.get('user_type') != 'staff':
        return jsonify({'success': False, 'message': 'Unauthorized'})

    new_status = 'Approved' if action == 'approve' else 'Rejected'
    
    # Get student email and item name BEFORE updating
    claim_details = execute_query("""
        SELECT s.email, s.name, li.item_name 
        FROM claims c
        JOIN student s ON c.student_id = s.student_id
        JOIN match_items m ON c.match_id = m.match_id
        JOIN lost_items li ON m.lost_item_id = li.lost_item_id
        WHERE c.claim_id = %s
    """, (claim_id,), fetch=True, fetchone=True)
    

    execute_query("UPDATE claims SET approval_status = %s, verified_by_staff_id = %s WHERE claim_id = %s",
                  (new_status, session['user_id'], claim_id))

    if new_status == 'Approved':

        execute_query("""
            UPDATE match_items m
            JOIN claims c ON c.match_id = m.match_id
            JOIN lost_items l ON l.lost_item_id = m.lost_item_id
            JOIN found_items f ON f.f_i_id = m.f_i_id
            SET m.status = 'Approved', l.status = 'Resolved', f.status = 'Claimed'
            WHERE c.claim_id = %s
        """, (claim_id,))
    else:
        # Mark the match as rejected (leave lost_items as 'Unresolved' / found_items as 'Unclaimed')
        execute_query("""
            UPDATE match_items m
            JOIN claims c ON c.match_id = m.match_id
            SET m.status = 'Rejected'
            WHERE c.claim_id = %s
        """, (claim_id,))

    # Send student-specific notification
    if claim_details:
        if new_status == 'Approved':
            student_notif = f"🎉 Congratulations! Your claim for '{claim_details['item_name']}' has been APPROVED. You can now collect your item."
        else:
            student_notif = f"❌ Your claim for '{claim_details['item_name']}' has been REJECTED. Please contact staff for more information."
        
        execute_query(
            "INSERT INTO notifications (message, date, status) VALUES (%s, CURDATE(), 'Unread')",
            (f"[{claim_details['email']}] {student_notif}",)
        )

    # after_claim_update_notify trigger will insert the notification row automatically (if you have it)
    return jsonify({'success': True, 'message': f'Claim {new_status.lower()} successfully'})


@app.route('/staff/match-items', methods=['GET'])
def staff_match():
    """Staff view for lost–found matching (auto-suggestions + manual view)"""
    if 'user_id' not in session or session.get('user_type') != 'staff':
        return redirect(url_for('index'))

    # Fetch unresolved lost items
    lost_query = """
        SELECT li.lost_item_id, li.item_name, li.category, li.description,
               li.lost_date, li.lost_loc, li.status, li.photo,
               s.name AS student_name, s.email AS student_email
        FROM lost_items li
        JOIN student s ON li.student_id = s.student_id
        WHERE li.status = 'Unresolved'
        ORDER BY li.lost_date DESC
    """
    lost_items = execute_query(lost_query, fetch=True) or []

    # Fetch unclaimed found items
    found_query = """
        SELECT f.f_i_id, f.item_name, f.category, f.description,
               f.found_date, f.found_loc, f.status, f.photo,
               CASE WHEN f.report_student_id IS NOT NULL THEN s.name ELSE st.name END AS reporter_name
        FROM found_items f
        LEFT JOIN student s ON f.report_student_id = s.student_id
        LEFT JOIN staff st ON f.report_staff_id = st.staff_id
        WHERE f.status = 'Unclaimed'
        ORDER BY f.found_date DESC
    """
    found_items = execute_query(found_query, fetch=True) or []

    # Fetch existing matches
    match_query = """
        SELECT m.match_id,
               DATE_FORMAT(m.match_date, '%Y-%m-%d') AS match_date,
               m.status,
               li.item_name AS lost_item_name,
               fi.item_name AS found_item_name
        FROM match_items m
        JOIN lost_items li ON m.lost_item_id = li.lost_item_id
        JOIN found_items fi ON m.f_i_id = fi.f_i_id
        ORDER BY m.match_date DESC
    """
    matches = execute_query(match_query, fetch=True) or []

    # Auto-match suggestion logic
    def similarity(a, b):
        return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

    suggestions = []
    for lost in lost_items:
        lost_date = lost.get("lost_date")
        try:
            lost_date_obj = datetime.strptime(str(lost_date), "%Y-%m-%d")
        except Exception:
            lost_date_obj = None

        for found in found_items:
            # Compute name similarity
            score = similarity(lost["item_name"], found["item_name"])

            # Compare category and location
            same_category = lost["category"] == found["category"]
            loc_match = lost["lost_loc"].lower() in found["found_loc"].lower() or \
                        found["found_loc"].lower() in lost["lost_loc"].lower()

            # Date closeness check
            try:
                found_date_obj = datetime.strptime(str(found["found_date"]), "%Y-%m-%d")
                date_diff = abs((found_date_obj - lost_date_obj).days) if lost_date_obj else 999
            except Exception:
                date_diff = 999

            # Apply thresholds
            if score > 0.7 and same_category and date_diff <= 7:
                suggestions.append({
                    "lost_id": lost["lost_item_id"],
                    "found_id": found["f_i_id"],
                    "lost_name": lost["item_name"],
                    "found_name": found["item_name"],
                    "lost_loc": lost["lost_loc"],
                    "found_loc": found["found_loc"],
                    "category": lost["category"],
                    "date_diff": date_diff,
                    "similarity": round(score * 100, 1)
                })
                
                # Create student-specific notification for potential match
                student_email = lost.get("student_email")
                if student_email:
                    notif_msg = f"🎯 Potential match found for your lost item '{lost['item_name']}'! Staff can review and confirm this match."
                    execute_query(
                        "INSERT INTO notifications (message, date, status) VALUES (%s, CURDATE(), 'Unread')",
                        (f"[{student_email}] {notif_msg}",)
                    )
                
                # Global notification
                global_notif = f"Potential match found: Lost '{lost['item_name']}' ↔ Found '{found['item_name']}'"
                create_notification(global_notif)

    # Sort suggestions by best similarity first
    suggestions.sort(key=lambda x: x["similarity"], reverse=True)

    # Clean binary data from found_items before JSON serialization
    found_items_json = []
    for item in found_items:
        item_dict = dict(item)
        # Add flag to indicate if photo exists
        item_dict['has_photo'] = bool(item_dict.get('photo'))
        # Remove binary photo data to make it JSON serializable
        item_dict.pop('photo', None)
        found_items_json.append(item_dict)

    #  Render 
    return render_template(
        "staff_match.html",
        user_name=session["user_name"],
        lost_items=lost_items,
        found_items=found_items,
        found_items_json=found_items_json,
        matches=matches,
        suggestions=suggestions
    )

@app.route('/staff/confirm-match', methods=['POST'])
def confirm_match():
    """Staff confirms a match between a lost item and a found item.
       Expects JSON: { lost_item_id: int, found_item_id: int } OR form data.
       Inserts into match_items, updates statuses, and creates a notification.
    """
    if 'user_id' not in session or session.get('user_type') != 'staff':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    # Accept JSON or form-encoded POST
    data = None
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    try:
        lost_item_id = int(data.get('lost_item_id'))
        found_item_id = int(data.get('found_item_id'))
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid parameters'}), 400

    # Get names (for notification) and verify existence/status
    lost_row = execute_query("SELECT item_name, status FROM lost_items WHERE lost_item_id = %s",
                             (lost_item_id,), fetch=True, fetchone=True)
    found_row = execute_query("SELECT item_name, status FROM found_items WHERE f_i_id = %s",
                              (found_item_id,), fetch=True, fetchone=True)

    if not lost_row or not found_row:
        return jsonify({'success': False, 'message': 'Item(s) not found'}), 404


    if lost_row.get('status') not in ['Unresolved', 'Matched']:
        return jsonify({'success': False, 'message': 'Lost item not available for matching'}), 409
    if found_row.get('status') not in ['Unclaimed', 'Matched']:
        return jsonify({'success': False, 'message': 'Found item not available for matching'}), 409

    try:
        # Insert match record
        insert_query = """
            INSERT INTO match_items (lost_item_id, f_i_id, match_date, status)
            VALUES (%s, %s, CURDATE(), 'Pending')
        """
        inserted = execute_query(insert_query, (lost_item_id, found_item_id))
        
        # Get match_id reliably:
        match_row = execute_query("""
            SELECT match_id FROM match_items
            WHERE lost_item_id = %s AND f_i_id = %s
            ORDER BY match_id DESC LIMIT 1
        """, (lost_item_id, found_item_id), fetch=True, fetchone=True)
        match_id = match_row['match_id'] if match_row else None

        
        # Get student email for targeted notification
        student_info = execute_query(
            "SELECT s.email, s.name FROM student s JOIN lost_items li ON s.student_id = li.student_id WHERE li.lost_item_id = %s",
            (lost_item_id,), fetch=True, fetchone=True
        )

        if student_info:
            # Notify the student whose item was matched
            student_notif = f"✅ Great news! Your lost item '{lost_row.get('item_name')}' has been matched with a found item '{found_row.get('item_name')}'. Please visit the Claim Item page to submit your claim!"
            execute_query(
                "INSERT INTO notifications (message, date, status) VALUES (%s, CURDATE(), 'Unread')",
                (f"[{student_info['email']}] {student_notif}",)
            )

        # Create notification for system (global notifications table)
        staff_name = session.get('user_name', 'Staff')
        notif_msg = f"Staff {staff_name} matched Lost '{lost_row.get('item_name')}' with Found '{found_row.get('item_name')}' (match_id={match_id})"
        execute_query("INSERT INTO notifications (message, date, status) VALUES (%s, CURDATE(), 'Unread')", (notif_msg,))

        return jsonify({'success': True, 'message': 'Match recorded', 'match_id': match_id})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating match: {e}'}), 500
    

# IMAGE SERVING ROUTES

@app.route('/image/lost/<int:item_id>')
def get_lost_image(item_id):
    """Serve lost item image"""
    query = "SELECT photo FROM lost_items WHERE lost_item_id = %s"
    result = execute_query(query, (item_id,), fetch=True, fetchone=True)
    
    if result and result['photo']:
        return send_file(io.BytesIO(result['photo']), mimetype='image/jpeg')
    return '', 404

@app.route('/image/found/<int:item_id>')
def get_found_image(item_id):
    """Serve found item image"""
    query = "SELECT photo FROM found_items WHERE f_i_id = %s"
    result = execute_query(query, (item_id,), fetch=True, fetchone=True)
    
    if result and result['photo']:
        return send_file(io.BytesIO(result['photo']), mimetype='image/jpeg')
    return '', 404

@app.route('/image/claim/<int:claim_id>')
def get_claim_proof(claim_id):
    """Serve claim proof image if non-empty"""
    query = "SELECT proof_file FROM claims WHERE claim_id = %s"
    result = execute_query(query, (claim_id,), fetch=True, fetchone=True)
    
    if result and result.get('proof_file'):

        return send_file(io.BytesIO(result['proof_file']), mimetype='image/jpeg')

    return '', 404


# API ROUTES FOR AJAX

@app.route('/api/notifications')
def get_notifications():
    """Get notifications for current user"""
    if 'user_id' not in session:
        return jsonify({'success': False})
    
    # Check if student or staff
    if session.get('user_type') == 'student':
        # Get student email for filtering
        student_query = "SELECT email FROM student WHERE student_id = %s"
        student = execute_query(student_query, (session['user_id'],), fetch=True, fetchone=True)
        student_email = student['email'] if student else None
        
        if student_email:
            query = """
                SELECT * FROM notifications 
                WHERE message LIKE %s OR message NOT LIKE '[%'
                ORDER BY date DESC LIMIT 20
            """
            notifications = execute_query(query, (f"[{student_email}]%",), fetch=True) or []
            
            # Clean up the email prefix
            for notif in notifications:
                if notif['message'].startswith(f"[{student_email}]"):
                    notif['message'] = notif['message'].replace(f"[{student_email}] ", "")
        else:
            notifications = []
    else:
        # Staff sees global notifications only
        query = """SELECT * FROM notifications WHERE message NOT LIKE '[%' OR message LIKE '[staff%' ORDER BY date DESC LIMIT 20"""
        notifications = execute_query(query, fetch=True) or []
    
    return jsonify({'success': True, 'notifications': notifications})


@app.route('/api/mark-notification-read/<int:notif_id>', methods=['POST'])
def mark_notification_read(notif_id):
    """Mark notification as read"""
    query = "UPDATE notifications SET status = 'Read' WHERE notification_id = %s"
    execute_query(query, (notif_id,))
    return jsonify({'success': True})


# RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=Config.APP_DEBUG, host='0.0.0.0', port=5000)