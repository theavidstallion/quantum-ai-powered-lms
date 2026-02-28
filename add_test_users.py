"""
Script to add test users to the Quantum LMS database
Run this to create additional student and teacher accounts for testing
"""
import sqlite3
import os

def add_test_users():
    # Check if database exists
    if not os.path.exists('users.db'):
        print("❌ Error: users.db not found. Run app.py first to create the database.")
        return
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Test students
    students = [
        ('student1', 'student123', 'Student', 'student1@umt.edu.pk'),
        ('student2', 'student123', 'Student', 'student2@umt.edu.pk'),
        ('student3', 'student123', 'Student', 'student3@umt.edu.pk'),
        ('john_doe', 'john123', 'Student', 'john@umt.edu.pk'),
        ('jane_smith', 'jane123', 'Student', 'jane@umt.edu.pk'),
    ]
    
    # Test teachers
    teachers = [
        ('teacher1', 'teacher123', 'Teacher', 'teacher1@umt.edu.pk'),
        ('teacher2', 'teacher123', 'Teacher', 'teacher2@umt.edu.pk'),
        ('dr_fatima', 'fatima123', 'Teacher', 'fatima@umt.edu.pk'),
        ('mr_zunnurain', 'zun123', 'Teacher', 'zunnurain@umt.edu.pk'),
    ]
    
    print("\n🔄 Adding test users to database...\n")
    
    added_count = 0
    exists_count = 0
    
    for user in students + teachers:
        try:
            c.execute('INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)', user)
            print(f"✅ Added {user[2]}: {user[0]} (password: {user[1]})")
            added_count += 1
        except sqlite3.IntegrityError:
            print(f"⚠️  User '{user[0]}' already exists")
            exists_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Summary:")
    print(f"   - New users added: {added_count}")
    print(f"   - Already existed: {exists_count}")
    print(f"   - Total attempted: {added_count + exists_count}")
    print("\n✅ Done! You can now login with these credentials.")
    print("\n📝 Sample credentials:")
    print("   Student: student1 / student123")
    print("   Teacher: teacher1 / teacher123")
    print("   Admin:   admin / admin123")

if __name__ == '__main__':
    add_test_users()
