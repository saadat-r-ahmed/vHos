from flask import Blueprint, render_template, request, redirect, session
owner = Blueprint("owner", __name__, static_folder = "static", template_folder = "templates")
import sql, hashlib
import datetime
from termcolor import colored
vo = owner
import json
# from main import mysql
# from flask_mysqldb import MySQL,MySQLdb 


# * VO authitication Working Properly ✅
# Saves the following the the session data
# vo_email
# vo_password
# vo_name
@owner.route('/authenticate_vo', methods = ['POST'])
def authenticate_vo():
    if request.method == "POST":
        email = request.form["id"]
        password = request.form["pass"]
        
        
        dbpass = sql.sql_data(f"select password from owner where email = '{email}';")
        if len(dbpass) == 0:
            return render_template('message.html',message = 'Login Failed', href = '/asp')


        elif dbpass[0][0] == password and len(dbpass) == 1:
            
            session['vo_email'] = email
            session['vo_password'] = password
            session['vo_name'] = sql.sql_data(f"select name from owner where email = '{email}'")[0][0]
            return redirect('vo_dashboard')

        else:
            return render_template('message.html',message = 'Login Failed', href = '/asp')


# * VO SignUp Working Properly ✅
@owner.route('/create_new_vo')
def create_new_vo():
    return render_template('signup_vo.html')


# * VO Dashboard Working Properly ✅
@owner.route('/owner_dashboard')
@owner.route('/vo_dashboard')
def vo_dashboard():
    if 'vo_email' in session:
        name = session['vo_name']
        return render_template('vo_dashboard.html', name = name, id = session['vo_email'])
    else:
        return redirect('login_owner')


# * VO Logout Working Properly ✅
@owner.route('/vo_logout')
def vo_logout():
    session.pop('vo_email', None)
    session.pop('vo_password', None)
    session.pop('vo_name', None)
    return redirect('login_owner')


# * VO data push Working Properly ✅
@owner.route('/make_vo', methods=['POST'])
def make_vo():
    email = request.form['email']
    name = request.form['name']
    long = request.form['long']
    lat = request.form['lat']
    psw = request.form['password']
    
    chq = sql.sql_data(f"select * from owner where email = '{email}'")
    
    if len(chq) == 0:
        query = 'insert into owner (email, name, longitude, latitude, password) values (%s, %s, %s, %s, %s)'
        

        val = (email, name, long, lat, psw)
        sql.insert(query, val)
        
        return render_template('message.html',message = 'Profile Created', href = '/owner')
    else:
        return render_template('message.html',message = 'Profile Already Exists, try again', href = '/create_new_vo')


# * VO Show Service Working Properly ✅
@vo.route('/vo/show_services')
@vo.route('/vo_dashboard/show_services')
def show_services():
    if 'vo_email' in session:
        services = sql.sql_dict(f"SELECT services.asp_id as 'asp_id', asp_data.name as 'name_asp', service_name as 'service_name', asp_data.address as address, price as 'price', description as 'description' FROM services INNER JOIN asp_data ON services.asp_id = asp_data.asp_id ORDER BY services.asp_id;") 
        return render_template('vo_show_services.html', id = session['vo_name'], services = services)
    else:
        return redirect('/vo')

# * VO Regular Service Request Working Properly ✅
@vo.route('/vo_regular_request', methods = ['POST'])
def vo_regular_request():
    if 'vo_email' in session:
        req_id = sql.sql_data('select max(request_id) from regular')
        if req_id[0][0] == None:
            req_id = 0
        else:
            req_id = str(int(req_id[0][0]) + 1)
        asp_id = request.form['asp_id']
        service = request.form['service']
        sql.sql(f"INSERT INTO regular (request_id, vo_id, asp_id, service_name) VALUES ('{req_id}', '{session['vo_email']}', '{asp_id}', '{service}');")
        return render_template('message.html',message = 'Request Placed.', href = '/vo/show_services')
    else:
        return redirect('/vo')

@vo.route('/regular_requests_status')
def regular_requests_status():
    if 'vo_email' in session:
        requests = sql.sql_dict(f"select * from regular where vo_id = '{session['vo_email']}' order by status")
        return render_template('vo_all_regular_request.html', requests = requests)
    else:
        redirect('/vo')
        
        
# * VO Emergency Request Working Properly ✅
@vo.route('/vo/emergency_request_page')
def emergency_request_page():
    if 'vo_email' in session:
        return render_template('vo_emergency_request.html')

@vo.route('/make_emergency_request', methods=['POST'])
def make_emergency_request():
    if 'vo_email' in session:
        vo_id = session['vo_email']
        location = request.form['location']
        req_id = sql.sql_data('select max(request_id) from request')
        if req_id[0][0] == None:
            req_id = 0
        else:
            req_id = str(int(req_id[0][0]) + 1)
        sql.sql(f"INSERT INTO request (request_id, vo_id, location) VALUES ('{req_id}', '{vo_id}','{location}');")
        return render_template('message.html',message = 'Emergency Request Placed.', href = '/vo/emergency_request_page')
    else:
        return redirect('/vo')

# * VO Emergency Request Working Properly ✅
@vo.route('/emergency_requests_status')
def emergency_requests_status():
    if 'vo_email' in session:
        qry = f"select * from request where vo_id = '{session['vo_email']}' order by status"
        requests = sql.sql_dict(qry)
        return render_template('vo_all_emergency_request.html', requests = requests)
    else:
        redirect('/vo')


@vo.route('/vo/review_asp')
def review_asp():
    if 'vo_email' in session:
        q = f"select * from cars where vo_mail = '{session['vo_email']}' order by status"
        cases = sql.sql_dict(q)
        return render_template('vo_review.html', cases = cases)
    else:
        redirect('/vo')
        
@vo.route('/vo_send_review', methods = ['POST'])
def vo_send_review():
    if 'vo_email' in session:
        v_id = request.form['v_id']
        review = request.form['review']
        sql.sql(f"update cars set review = '{review}' where v_id = '{v_id}'")
        return redirect('/vo/review_asp')


@vo.route('/vo_profile_edit_request')
def vo_profile_edit_request():
    if 'vo_email' in session:
        return render_template('vo_profile_edit_request.html' , email = session['vo_email'], name = session['vo_name'])
    else:
        return redirect('/vo')
 
@vo.route('/commit_vo_update', methods = ['POST'])
def commit_vo_update():
    if 'vo_email' in session:
        name = request.form['name']
        longitude = request.form['longitude']
        latitude = request.form['latitude']
        password = request.form['password']
                
        if name != '':
            qry = f"UPDATE owner SET name = '{name}' WHERE email = '{session['vo_email']}';"
            sql.update(qry)
            session['vo_name'] = name
        if password != '':
            qry = f"UPDATE owner SET password = '{password}' WHERE email = '{session['vo_email']}';"
            sql.update(qry)
            session['vo_password'] = password
 
        if longitude != '':
            qry = f"UPDATE owner SET longitude = '{longitude}' WHERE email = '{session['vo_email']}';"
            sql.update(qry)
            session['vo_longitude'] = longitude
 
        if latitude != '':
            qry = f"UPDATE owner SET latitude = '{latitude}' WHERE email = '{session['vo_email']}';"
            sql.update(qry)
            session['vo_latitude'] = latitude

        return render_template('message.html', message = 'UPDATED', href = 'vo_profile_edit_request')
    else:
        return redirect('/vo')