# Basic  imports
from flask import Flask, render_template, url_for, request, redirect, session, json
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from datetime import datetime
from admin import admin
from asp import asp
from owner import owner

# User defined module imports
# from sql import insert_into_marks, insert_into_teacher,  insert_into_assesment
# from sql import fetch_all_marks, insert_into_enroll, fetch_all_assesment
# from sql import sql, fetch_sql, del_student_db, del_teacher_db





app = Flask(__name__)
app.register_blueprint(admin, url_prefix='')
app.register_blueprint(asp, url_prefix='')
app.register_blueprint(owner, url_prefix='')

app.secret_key = "team-6"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vhos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)



@app.route('/')
def main():
    return render_template('homepage.html')


@app.route('/homepage')
@app.route('/home')
def homepahe():
    return render_template('home.html')




@app.route('/admin')
@app.route('/login_admin')
def login_admin():
    if 'admin_id' in session:
        return redirect('admin_dashboard')
    return render_template('login_admin.html')

@app.route('/asp')
@app.route('/login_asp')
def login_asp():
    if 'asp_id' in session:
        return redirect('asp_dashboard')
    return render_template('asp_login.html')


@app.route('/vo')
@app.route('/services')
@app.route('/owner')
@app.route('/login_owner')
def login_owner():
    if 'vo_email' in session:
        return redirect('owner_dashboard')
    return render_template('vo_login.html')


@app.route('/about')
@app.route('/about_page')
def about():
    return render_template('about_page.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')




if __name__ == '__main__':
    app.run(debug=True)
