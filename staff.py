from enum import unique
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///staff.db'
db = SQLAlchemy(app)

class Staff(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(length=30), nullable=False, unique=True)
    PhoneNumber = db.Column(db.Integer(), nullable=False)
    Dob = db.Column(db.String(length=30), nullable=False)
    DoJoin = db.Column(db.String(length=30), nullable=False, unique=True)
    Email = db.Column(db.String(length=30), nullable=False, unique=True)

    def __init__(self, Name, PhoneNumber, Dob, DoJoin, Email):
      self.Name = Name
      self.PhoneNumber = PhoneNumber
      self.Dob = Dob
      self.DoJoin = DoJoin
      self.Email = Email



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/manage')
def manage_page():
    staffs = Staff.query.all()
    return render_template('manage.html', staffs=staffs)

@app.route('/add', methods = ['GET', 'POST'])
def add():
   if request.method == 'POST':
      Staffs = Staff(request.form['Name'], 
      request.form['PhoneNumber'],
      request.form['Dob'], 
      request.form['DoJoin'],
      request.form['Email'])
      
      db.session.add(Staffs)
      db.session.commit()

      return redirect(url_for('manage_page'))
   return render_template('add.html')

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
   staffs = Staff.query.filter_by(id = id).first()
   if request.method =='POST':
      db.session.delete(staffs)
      db.session.commit()
      return redirect(url_for('manage_page'))
   return render_template('delete.html')

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
   staffs = Staff.query.filter_by(id = id).first()

   if request.method == 'POST':
      staffs.Name = request.form['Name']
      staffs.PhoneNumber = request.form['PhoneNumber']
      staffs.Dob = request.form['Dob']
      staffs.DoJoin = request.form['DoJoin']
      staffs.Email = request.form['Email']

      db.session.merge(staffs)
      db.session.commit()

      return redirect(url_for('manage_page'))
   return render_template('edit.html')

