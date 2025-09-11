# Flask Database Relationships

This project demonstrates how to establish **relationships between
database models** in a Flask application using **Flask-SQLAlchemy**.

## Relationships Covered

### 1. One-to-Many

Example: **User → Post**

``` python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### 2. Many-to-Many

Example: **Student ↔ Course**

``` python
student_course = db.Table(
    'student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    courses = db.relationship('Course', secondary=student_course,
                              backref=db.backref('students', lazy='dynamic'))
```

### 3. One-to-One

Example: **User ↔ UserProfile**

``` python
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    profile = db.relationship('UserProfile', backref='user', uselist=False)
```

## Usage

``` bash
flask db init
flask db migrate
flask db upgrade
```

Then run your Flask app and interact with the database as shown in the
examples.

------------------------------------------------------------------------

**License**: MIT
