#from app import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model,UserMixin):
   # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(100),unique=True)
    email = db.Column(db.String(20),unique=True)
    number = db.Column(db.String(20),unique=True)
    Fname = db.Column(db.String(20), nullable=True)
    Lname = db.Column(db.String(20), nullable=True)
    courses = db.relationship('Courses',backref='course',lazy=True)
    #SIC = db.relationship('StudentsInCourses',backref='sic',lazy=True)
    type = db.Column(db.Integer(),nullable=True)
    #SIC = db.relationship('StudentsInCourses',backref='sic',lazy=True)


class Courses(db.Model):
    #id = db.Column(db.Integer(),primary_key=True)
    CourseName = db.Column(db.String(40),primary_key=True)
    coursecategory = db.Column(db.String(40))
    coursedescription = db.Column(db.String(300))
    Iusername = db.Column(db.String(20),db.ForeignKey('user.username'))
    #courname = db.relationship('StudentsInCourses',backref='courssename',lazy=True)
    idforvid = db.relationship('studentAnalysis',backref='vidid2',lazy=True)

class StudentsInCourses(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    coursename =  db.Column(db.String(40),db.ForeignKey('courses.CourseName'))
    Susername = db.Column(db.String(20),db.ForeignKey('user.username'))

class Videosincourses(db.Model):
    #id = db.Column(db.Integer())
    coursename =  db.Column(db.String(40),db.ForeignKey('courses.CourseName'))
    vidName = db.Column(db.String(40),primary_key=True)
    idforvid = db.relationship('studentAnalysis',backref='vidid',lazy=True)


class studentAnalysis(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    vidname = db.Column(db.String(40),db.ForeignKey('videosincourses.vidName'))
    courseName = db.Column(db.String(40),db.ForeignKey('courses.CourseName'))
    Susername = db.Column(db.String(20),db.ForeignKey('user.username'))
    engState = db.Column(db.Integer())