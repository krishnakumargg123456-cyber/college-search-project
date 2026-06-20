import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS colleges 
          (id INTEGER PRIMARY KEY , name TEXT  UNIQUE, city TEXT, fees INTEGER, avg_package REAL, placement INTEGER, ranking INTEGER)''')

# College data: name, city, fees, avg_package, placement, ranking
colleges = [
    # IIT - 23
    ('IIT Bombay', 'Mumbai', 250000, 25.5, 95, 1),
    ('IIT Delhi', 'Delhi', 260000, 24.8, 96, 2),
    ('IIT Madras', 'Chennai', 240000, 22.3, 94, 3),
    ('IIT Kanpur', 'Kanpur', 230000, 21.5, 93, 4),
    ('IIT Kharagpur', 'Kharagpur', 220000, 20.8, 92, 5),
    ('IIT Roorkee', 'Roorkee', 210000, 19.2, 90, 6),
    ('IIT Guwahati', 'Guwahati', 200000, 18.5, 89, 7),
    ('IIT Hyderabad', 'Hyderabad', 240000, 22.1, 91, 8),
    ('IIT BHU', 'Varanasi', 180000, 16.5, 88, 9),
    ('IIT Indore', 'Indore', 230000, 19.8, 87, 10),
    ('IIT Gandhinagar', 'Gandhinagar', 220000, 17.5, 85, 11),
    ('IIT Bhubaneswar', 'Bhubaneswar', 190000, 15.2, 83, 12),
    ('IIT Patna', 'Patna', 180000, 14.8, 82, 13),
    ('IIT Mandi', 'Mandi', 170000, 14.2, 80, 14),
    ('IIT Jodhpur', 'Jodhpur', 200000, 16.8, 84, 15),
    ('IIT Ropar', 'Ropar', 190000, 15.5, 81, 16),
    ('IIT Dhanbad', 'Dhanbad', 170000, 13.5, 78, 17),
    ('IIT Tirupati', 'Tirupati', 180000, 12.8, 76, 18),
    ('IIT Palakkad', 'Palakkad', 175000, 12.2, 75, 19),
    ('IIT Goa', 'Goa', 190000, 14.5, 79, 20),
    ('IIT Bhilai', 'Bhilai', 170000, 11.8, 74, 21),
    ('IIT Jammu', 'Jammu', 175000, 12.5, 73, 22),
    ('IIT Dharwad', 'Dharwad', 170000, 11.5, 72, 23),

    # NIT - 31
    ('NIT Trichy', 'Tiruchirappalli', 150000, 12.8, 92, 9),
    ('NIT Surathkal', 'Surathkal', 145000, 11.5, 90, 10),
    ('NIT Warangal', 'Warangal', 150000, 12.5, 91, 11),
    ('NIT Rourkela', 'Rourkela', 140000, 10.8, 88, 12),
    ('NIT Calicut', 'Calicut', 135000, 10.2, 87, 13),
    ('NIT Durgapur', 'Durgapur', 130000, 8.5, 82, 20),
    ('NIT Silchar', 'Silchar', 125000, 8.2, 80, 22),
    ('NIT Kurukshetra', 'Kurukshetra', 140000, 9.8, 85, 15),
    ('NIT Jamshedpur', 'Jamshedpur', 130000, 8.8, 83, 18),
    ('NIT Hamirpur', 'Hamirpur', 135000, 9.2, 84, 17),
    ('NIT Allahabad', 'Prayagraj', 145000, 11.2, 89, 14),
    ('NIT Jaipur', 'Jaipur', 140000, 10.5, 86, 16),
    ('NIT Bhopal', 'Bhopal', 135000, 9.5, 83, 19),
    ('NIT Nagpur', 'Nagpur', 140000, 10.8, 87, 15),
    ('NIT Jalandhar', 'Jalandhar', 130000, 8.5, 81, 21),
    ('NIT Delhi', 'Delhi', 150000, 12.2, 88, 13),
    ('NIT Goa', 'Goa', 145000, 10.2, 82, 18),
    ('NIT Puducherry', 'Puducherry', 135000, 8.8, 80, 23),
    ('NIT Uttarakhand', 'Srinagar', 130000, 7.5, 75, 28),
    ('NIT Manipur', 'Imphal', 125000, 6.8, 72, 32),
    ('NIT Meghalaya', 'Shillong', 130000, 7.2, 74, 30),
    ('NIT Mizoram', 'Aizawl', 120000, 6.2, 70, 35),
    ('NIT Nagaland', 'Dimapur', 120000, 6.0, 68, 36),
    ('NIT Sikkim', 'Ravangla', 125000, 6.5, 71, 33),
    ('NIT Arunachal Pradesh', 'Yupia', 120000, 6.0, 69, 37),
    ('NIT Andhra Pradesh', 'Tadepalli', 140000, 9.2, 82, 20),
    ('NIT Agartala', 'Agartala', 125000, 7.0, 73, 31),

    # GFTI - 8
    ('BIT Mesra', 'Ranchi', 180000, 11.5, 85, 25),
    ('PEC Chandigarh', 'Chandigarh', 160000, 10.2, 83, 28),
    ('Thapar University', 'Patiala', 400000, 12.8, 88, 22),
    ('IIIT Allahabad', 'Prayagraj', 180000, 18.5, 92, 12),
    ('IIIT Delhi', 'Delhi', 220000, 19.2, 93, 11),
    ('IIIT Hyderabad', 'Hyderabad', 250000, 22.5, 94, 8),
    ('NSUT Delhi', 'Delhi', 170000, 14.5, 90, 16),
    ('DTU Delhi', 'Delhi', 180000, 12.3, 88, 15),

    # Top Private - 50+
    ('VIT Vellore', 'Vellore', 400000, 8.2, 85, 15),
    ('SRM Chennai', 'Chennai', 350000, 7.8, 80, 25),
    ('Manipal Institute', 'Manipal', 380000, 8.5, 82, 20),
    ('BITS Pilani', 'Pilani', 500000, 18.5, 92, 10),
    ('Amity Noida', 'Noida', 300000, 6.5, 75, 40),
    ('LPU Punjab', 'Jalandhar', 250000, 6.2, 72, 45),
    ('Shiv Nadar', 'Greater Noida', 450000, 11.5, 85, 18),
    ('Ashoka University', 'Sonipat', 600000, 9.8, 78, 30),
    ('GLA University', 'Mathura', 220000, 6.5, 75, 50),
    ('Bennett University', 'Greater Noida', 420000, 8.8, 80, 35),
    ('UPES Dehradun', 'Dehradun', 320000, 7.2, 76, 42),
    ('KIIT Bhubaneswar', 'Bhubaneswar', 280000, 7.0, 78, 38),
]

# Insert data
for college in colleges:
    c.execute('''INSERT OR IGNORE INTO colleges 
                (name, city, fees, avg_package, placement, ranking) 
                VALUES (?, ?, ?, ?, ?, ?)''', college)

conn.commit()
conn.close()
print(f"✅ {len(colleges)} colleges added successfully to database.db!")