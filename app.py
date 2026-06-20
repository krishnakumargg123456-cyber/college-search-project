
from flask import Flask,render_template,request,redirect,url_for,session,flash # pyright: ignore[reportMissingImports]
from ai_recommend import recommend_colleges


import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'database/colleges.db'
os.makedirs('database', exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Table ban jayega auto
with get_db() as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT)')
    conn.commit()



app = Flask(__name__)
app.secret_key = "collegefinder"

@app.route("/")
def home():
    return render_template("college.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password)

        try:
            with get_db() as conn:  # <-- ye wala with
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed_pw)
                )
                conn.commit()
            flash('Register ho gaya! Ab login kar')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Ye email pehle se hai')
            return redirect(url_for('register'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        with get_db() as conn:  # <-- yaha bhi with
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            flash('Email ya password galat')
            return redirect(url_for('login'))
    
    return render_template("login.html")
        

    

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user={"name": session["user"]} 
    )

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

@app.route("/colleges")
def colleges():

    conn = sqlite3.connect(
        "database/colleges.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM colleges"
    )

    colleges = cursor.fetchall()

    conn.close()

    return render_template(
        "colleges.html",
        colleges=colleges
    )
@app.route("/college/<int:college_id>")
def college_detail(college_id):
    return render_template("college_detail.html", college_id=college_id)

    @app.route("/search")
    def search():
        keyword = request.args.get("keyword", "")  # <- ye line zaroori hai
    
    conn = sqlite3.connect("database/colleges.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM colleges WHERE name LIKE ?", (f"%{keyword}%",))
    colleges = cursor.fetchall()
    conn.close()
    
    return render_template("colleges.html", colleges=colleges)

    conn = sqlite3.connect(
        "database/colleges.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM colleges WHERE id=?",
        (college_id,)
    )

    college = cursor.fetchone()

    conn.close()

    return render_template(
        "college_detail.html",
        college=college
    )
    return redirect("/")
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        budget = request.form.get('budget')
        city = request.form.get('city')
        branch = request.form.get('branch')
        placement = request.form.get('placement')

        if not budget:
            return render_template('recommend.html', error="Budget dalna jaruri hai!")

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # BUDGET KO INTEGER ME CONVERT KARO - Ye main fix hai
        try:
            budget = int(budget)
        except:
            return render_template('recommend.html', error="Budget number me dalo!")

        # Base query
        query = "SELECT * FROM colleges WHERE fees <=?"
        params = [budget]

        # City sirf tab add karo jab user ne kuch likha ho
        if city and city.strip()!= "":
            query += " AND city LIKE?"
            params.append(f'%{city.strip()}%')

        # Placement filter bhi add karo agar dala ho
        if placement and placement.strip()!= "":
            try:
                query += " AND placement >=?"
                params.append(int(placement))
            except:
                pass

        # LIMIT badha di 10 kar di
        query += " ORDER BY placement DESC, ranking ASC LIMIT 10"

        print("Final Query:", query) # Debug ke liye
        print("Params:", params)

        c.execute(query, params)
        colleges = c.fetchall()
        conn.close()

        print("Colleges found:", len(colleges)) # Terminal me dikhega

        if not colleges:
            return render_template('recommend.html', error=f"₹{budget:,} budget me college nahi mila. Budget badhao ya city/placement khali chhod do")

        return render_template('recommend.html', colleges=colleges, result=f"AI ne {len(colleges)} college dhoond liye!")

    return render_template('recommend.html')

    # GET request - khali form dikhao
    return render_template('recommend.html')

@app.route('/predictor', methods=['GET', 'POST'])
def predictor():
    result = ""
    if request.method == "POST":
        marks = float(request.form["marks"])
        category = request.form["category"]
        course = request.form["course"]
        
        if marks >= 90:
            result = f"Top tier colleges me chance hai {course} ke liye!"
        elif marks >= 75:
            result = f"{category} category me achhe colleges mil jayenge"
        elif marks >= 60:
            result = f"Tier-2/3 colleges best rahenge {course} ke liye"
        else:
            result = "Score improve karo ya diploma courses try karo"
    
    return render_template("predictor.html", result=result)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    college1 = None
    college2 = None
    error = None
    
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
    except Exception as e:
        error = f"Database connection error: {e}"
        return render_template('compare.html', college1=None, college2=None, error=error)

    if request.method == 'POST':
        name1 = request.form.get('college1', '').strip()
        name2 = request.form.get('college2', '').strip()
        
        print("Form input:", name1, "|", name2)

        if not name1 or not name2:
            error = "Please enter both college names"
        else:
            # College 1 search + auto add
            c.execute("SELECT * FROM colleges WHERE LOWER(name) LIKE LOWER(?) LIMIT 1", ('%' + name1 + '%',))
            college1 = c.fetchone()
            if not college1:
                c.execute("INSERT INTO colleges (name, city, fees, avg_package, placement, ranking) VALUES (?, 'N/A', 0, 0.0, 0, 0)", (name1,))
                conn.commit()
                c.execute("SELECT * FROM colleges WHERE name = ?", (name1,))
                college1 = c.fetchone()
                print(f"Auto-added: {name1}")

            # College 2 search + auto add  
            c.execute("SELECT * FROM colleges WHERE LOWER(name) LIKE LOWER(?) LIMIT 1", ('%' + name2 + '%',))
            college2 = c.fetchone()
            if not college2:
                c.execute("INSERT INTO colleges (name, city, fees, avg_package, placement, ranking) VALUES (?, 'N/A', 0, 0.0, 0, 0)", (name2,))
                conn.commit()
                c.execute("SELECT * FROM colleges WHERE name = ?", (name2,))
                college2 = c.fetchone()
                print(f"Auto-added: {name2}")

    conn.close()
    return render_template('compare.html', college1=college1, college2=college2, error=error)

@app.route('/scholarship', methods=['GET'])
def scholarship():
    category = request.args.get('category', 'all')
    course_for = request.args.get('course_for', 'all') # NEW: kis liye filter
    search = request.args.get('search', '').strip()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Table check + data insert - tumhara wala hi code
    try:
        c.execute("SELECT id, name, provider, eligibility, amount, last_date, link, category, logo FROM scholarships ORDER BY last_date ASC")
        scholarships = c.fetchall()
    except:
        c.execute('''CREATE TABLE IF NOT EXISTS scholarships
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT, provider TEXT, eligibility TEXT,
                     amount TEXT, last_date TEXT, link TEXT,
                     category TEXT, logo TEXT)''')

        premium_data = [
            ('NSP Post Matric Scholarship', 'Govt of India', 'SC/ST/OBC, Income < 2.5L/year, 50%+ marks', '₹10,000 - ₹50,000/year', '2026-12-31', 'https://scholarships.gov.in', 'government', '🏛️'),
            ('UP Scholarship Dashottar', 'UP Govt', 'UP domicile, All categories, Income < 2L', 'Full fees + ₹3000/year', '2026-11-15', 'https://scholarship.up.gov.in', 'government', '🏛️'),
            ('AICTE Pragati Scholarship', 'AICTE', 'Girls only, Technical courses, Income < 8L', '₹50,000/year + Tuition', '2026-11-30', 'https://aicte-india.org', 'girls', '👩‍🎓'),
            ('Saksham Scholarship', 'AICTE', 'Disabled students >40%, B.Tech/Degree', '₹50,000/year', '2026-11-30', 'https://aicte-india.org', 'special', '♿'),
            ('Reliance Foundation UG', 'Reliance Foundation', 'Class 12 > 60%, JEE rank, Income < 15L', '₹6,00,000 for 4 years', '2026-10-20', 'https://reliancefoundation.org', 'merit', '💎'),
            ('Tata Trusts Scholarship', 'Tata Trusts', 'Merit + Need based, UG/PG all streams', '₹1,00,000 - ₹3,00,000', '2026-09-30', 'https://tatatrusts.org', 'merit', '🏆'),
            ('INSPIRE SHE Scholarship', 'DST Govt', 'Top 1% in Class 12, Science stream', '₹80,000/year', '2026-12-15', 'https://online-inspire.gov.in', 'government', '🔬'),
            ('Siemens Scholarship', 'Siemens India', 'Engineering students, Family income < 8L', '₹2,00,000/year', '2026-10-10', 'https://siemens.co.in', 'private', '⚡')
        ]
        c.executemany("INSERT INTO scholarships (name, provider, eligibility, amount, last_date, link, category, logo) VALUES (?,?,?,?,?,?,?,?)", premium_data)
        conn.commit()
        c.execute("SELECT id, name, provider, eligibility, amount, last_date, link, category, logo FROM scholarships ORDER BY last_date ASC")
        scholarships = c.fetchall()

    # SMART Filter + Search logic - sab option use honge
    filtered = []
    for s in scholarships:
        eligibility = s[3].lower()

        match_cat = (category == 'all' or s[7] == category)
        match_search = (not search or search.lower() in s[1].lower() or search.lower() in s[2].lower())

        # Kis liye scholarship filter - eligibility text check karega
        match_course = True
        if course_for == 'btech':
            match_course = any(k in eligibility for k in ['b.tech', 'technical', 'engineering', 'aicte', 'jee'])
        elif course_for == 'girls':
            match_course = 'girls' in eligibility or 'female' in eligibility
        elif course_for == 'scst':
            match_course = 'sc/st/obc' in eligibility
        elif course_for == 'disabled':
            match_course = 'disabled' in eligibility or 'saksham' in s[1].lower()
        elif course_for == 'merit':
            match_course = any(k in eligibility for k in ['merit', 'top 1%', 'jee rank', '60%', 'rank'])

        if match_cat and match_search and match_course:
            filtered.append(s)

    conn.close()
    return render_template('scholarships.html', scholarships=filtered, category=category, course_for=course_for, search=search)
def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS colleges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT,
        fees INTEGER,
        avg_package REAL,
        placement INTEGER,
        ranking INTEGER
    )''')
    
    # Sample data - pehle se hai to skip ho jayega
    c.execute("INSERT OR IGNORE INTO colleges (id, name, city, fees, avg_package, placement, ranking) VALUES (1, 'IIT Bombay', 'Mumbai', 250000, 25.5, 95, 1)")
    c.execute("INSERT OR IGNORE INTO colleges (id, name, city, fees, avg_package, placement, ranking) VALUES (2, 'DTU', 'Delhi', 180000, 12.3, 88, 5)")
    c.execute("INSERT OR IGNORE INTO colleges (id, name, city, fees, avg_package, placement, ranking) VALUES (3, 'NIT Trichy', 'Tiruchirappalli', 150000, 10.8, 90, 9)")
    
    conn.commit()
    conn.close()
    print("Table created + sample data added!")
if __name__=="__main__":
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)