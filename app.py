from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId  # Import ObjectId for MongoDB ID handling

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client.studentDB
students_collection = db.students

# Route to register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        data = {'name': name, 'age': age, 'email': email}
        
        # Insert data into MongoDB
        students_collection.insert_one(data)
        flash("Student registered successfully!")
        return redirect(url_for('view_students'))
    
    return render_template('register.html')

# Route to view all students
@app.route('/view')
def view_students():
    students = students_collection.find()
    return render_template('view.html', students=students)

# Route to edit student
@app.route('/edit/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'email': request.form['email']
        }
        
        students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_data})
        flash("Student information updated!")
        return redirect(url_for('view_students'))
    
    return render_template('edit.html', student=student)

# Route to delete student
@app.route('/delete/<student_id>')
def delete_student(student_id):
    students_collection.delete_one({"_id": ObjectId(student_id)})
    flash("Student deleted successfully!")
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(debug=True)
