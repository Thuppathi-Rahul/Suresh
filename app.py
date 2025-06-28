from flask import Flask, render_template, request, redirect, flash
from models import db, Student

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('student_form.html')

    @app.route('/submit', methods=['POST'])
    def submit():
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')

        if not name or not email or not department:
            return "Bad Request: Missing fields", 400

        student = Student(name=name, email=email, department=department)
        db.session.add(student)
        db.session.commit()
        flash('Student saved successfully!')
        return redirect('/')

    return app
