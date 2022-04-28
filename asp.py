from select import select
from flask import Blueprint, render_template, request, redirect, session, url_for
asp = Blueprint("asp", __name__, static_folder = "static", template_folder = "templates")
import sql, hashlib
import datetime
from termcolor import colored
# from pprint import pprint as print
import raw_sql
import json
from main import mysql
from flask_mysqldb import MySQL,MySQLdb

from table import table as t

# * Authinticate the ASP LOGIN✅ Working properly
# Stores the following in the session data
# asp_id
# asp_password
# asp_name
@asp.route('/authenticate_asp', methods = ['POST'])
def authenticate_asp():
    if request.method == "POST":
        asp_id = request.form["id"]
        password = request.form["pass"]
        dbpass = sql.sql_data(f"select password from asp_data where asp_id = '{asp_id}';")
        print(dbpass)
        if len(dbpass) == 0:
            return render_template('message.html',message = 'Login Failed', href = '/asp')
        elif dbpass[0][0] == password and len(dbpass) == 1:
            session['asp_id'] = asp_id
            session['asp_password'] = password
            session['asp_name'] = sql.sql_data(f"select name from asp_data where asp_id = '{asp_id}'")[0][0]
            return redirect('asp_dashboard')
        else:
            return render_template('message.html',message = 'Login Failed', href = '/asp')

# * Signup ASP ✅ Working properly
@asp.route('/asp_sign_up')
def asp_sign_up():
    return render_template('asp_sign_up.html', title_bar = "Signup")
 
@asp.route('/commit_asp_sign_up', methods = ['GET', 'POST'])
def commit_asp_sign_up():
    asp_id=request.form["asp_id"]
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    location=request.form["location"]
    address=request.form["address"]
    owner=request.form["owner"]
    chq = f'select * from asp_data where asp_id = "{asp_id}";'
    chq = sql.sql_data(chq)
    if len(chq) > 0:
        return render_template('message.html', message = 'A SERVICE PROVIDER ALREADY EXISTS WITH THIS ID, TRY ANOTHER ID.', href = '/asp_sign_up')
 
    else:
        qry = f"INSERT into asp_data values('{asp_id}','{name}','{owner}','{location}','{address}','{email}','{password}');"
        sql.sql(qry)
        return render_template('message.html', message = 'SUCCESSFULLY JOINED', href = '/asp')


# * ASP Dashboard  ✅ 🟡 Working properly || Might need to change later on
@asp.route('/asp_dashboard')
def asp_dashboard():
    if 'asp_id' in session:
        id = session['asp_id']
        name = session['asp_name']
        return render_template('asp_dashboard.html', id = id, name = name)
    else:
        return redirect('login_asp')


# * ASP Dashboard  ✅  Working properly
@asp.route('/asp_logout')
def asp_logout():
    session.pop('asp_id', None)
    session.pop('asp_password', None)
    session.pop('asp_name', None)
    return redirect('login_asp')


# * ASP ADD NEW SERVICE  ✅  Working properly
@asp.route('/asp/add_new_services')
def add_new_services():
    if 'asp_name' in session:
        return render_template('new_service_form.html', id = session['asp_id'])
    else:
        return redirect('/asp')


# * ASP ADD NEW SERVICE  ✅  Working properly
# Checks if the service already exists or not as well
@asp.route('/asp/add_service', methods=['POST'])
def add_service():
    if 'asp_id' in session:
        service_name = request.form["service_name"]
        price = request.form["price"]
        desc = request.form["desc"]
        id = session['asp_id']
        chq = sql.sql_data(f"select * from services where asp_id = '{id}' and service_name = '{service_name}'")
        if len(chq)>0:
            return render_template('message.html',message = 'Service already added. Go to edit services for editing details.', href = '/asp/add_new_services')
        else:
            query = 'insert into services (asp_id, service_name, price, description) values (%s, %s, %s, %s)'
            val = (session['asp_id'], service_name, price, desc)
            sql.insert(query, val)
            return render_template('message.html',message = 'Service Added', href = '/asp/add_new_services')
    else:
        return redirect('/asp')


# * Editorial page for ASP  ✅  Working properly
@asp.route('/asp/edit_prev_services')
def edit_prev_services():
    if 'asp_name' in session:
        id = session['asp_id']
        s = sql.sql_dict(f'select service_name, price, description from services where asp_id = "{id}"')
        return render_template('edit_prev_service.html', id = session['asp_id'], services = s)
    else:
        return redirect('/asp')


@asp.route('/asp/update_status')
def update_status():
    if 'asp_id' in session:
        id = session['asp_id']
        table = sql.sql_dict(f'select vo_mail as "VO Mail", v_id as "Vehicle ID", status as Status, review as "Review" from cars where asp_id = "{id}" ORDER BY Status desc')
        x = sql.sql_data(f'select DISTINCT vo_mail from cars where asp_id = "{id}" and status != "completed-100" ORDER BY Status desc;')
        v_id = []
        for i in x:
            v_id.append(i[0])
        if len(table) == 0:
            return render_template('message.html',message = 'No vehicle in the queue.', href = '/asp')
        else:
            return render_template('asp_update_status.html', id = id, table = table, v_id = v_id)



# * Status Update Form  ✅  Working properly
@asp.route('/asp_update_status_request' , methods = ['POST'])
def asp_update_status_request():
    if 'asp_id' in session:
        id = session['asp_id']
        vo_mail = request.form['vo_mail']
        v_id = request.form['v_id']
        status = request.form['status']
        chq = sql.sql_dict(f"select * from cars where vo_mail = '{vo_mail}' and v_id = '{v_id}' and asp_id = '{id}'")
        if len(chq)>0:
            qry = f"UPDATE cars SET status = '{status}' WHERE vo_mail = '{vo_mail}' and v_id = '{v_id}' and asp_id = '{id}';"
            sql.sql(qry)
            return render_template('message.html',message = 'Status Updated', href = '/asp/update_status')
        else:
            return render_template('message.html',message = 'Does not exist', href = '/asp/update_status')
    else:
        return redirect('/asp')


@asp.route('/asp/show_requests')
def show_requests():
    if 'asp_name' in session:
        id = session['asp_id']
        s = sql.asp_all_requests(f"select request_id, vo_id, location from request where status = 'Pending'")
        return render_template('asp_view_requests.html', id = session['asp_id'], services = s)
    else:
        return redirect('/asp')


@asp.route('/asp_accept_request' , methods = ['POST'])
def asp_accept_request():
    if 'asp_id' in session:
        id = session['asp_id']
        request_id = request.form['request_id']
        from datetime import datetime
        time = datetime.now()
        qry = f"UPDATE request set status = 'Accepted', asp_id = '{id}', time = '{time}' where request_id = '{request_id}'"
        sql.sql(qry)
        return render_template('message.html',message = 'Request Acceepted', href = '/asp/show_requests')

    else:
        return redirect('/asp')


# * ASP Update Service  ✅  Working properly
@asp.route('/update_service', methods = ['POST'])
def update_service():

    pk = request.form['pk']
    name = request.form['name']
    value = request.form['value']
    id = session['asp_id']

    if name == 'price':
        qry = f"UPDATE services SET price = '{value}' WHERE service_name ='{pk}' AND asp_id = '{id}'"
        sql.sql(qry)
        return redirect('/asp/edit_prev_services')

    elif name == 'description':
        qry = f"UPDATE services SET description = '{value}' WHERE service_name ='{pk}' AND asp_id = '{id}'"
        sql.sql(qry)
        return redirect('/asp/edit_prev_services')


# * ASP Delete Service  ✅  Working properly
@asp.route('/delete_service', methods=['POST'])
def delete_service():
    if 'asp_id' in session:
        name = request.form['service_name']
        sql.del_service_db(session['asp_id'], name)
        return render_template('message.html',message = 'Service Dropped.', href = '/asp/edit_prev_services')
    else:
        return redirect('/asp/edit_prev_services')
    


# * ASP edit Own Profile  ✅  Working properly
@asp.route('/asp_profile_edit_request')
def asp_profile_edit_request():
    if 'asp_id' in session:
        return render_template('asp_edit_profile.html' , id = session['asp_id'], name = session['asp_name'])
    else:
        return redirect('/asp')
 
 
# * ASP edit Own Profile  ✅  Working properly
@asp.route('/commit_asp_update', methods = ['POST'])
def commit_asp_update():
    if 'asp_id' in session:
        name = request.form['name']
        owner = request.form['owner']
        location=request.form['location']
        address=request.form['address']
        email=request.form['email']
        password = request.form['password']
        if name != '':
            qry = f"UPDATE asp_data SET name = '{name}' WHERE asp_id = '{session['asp_id']}';"
            sql.sql(qry)
            session['asp_name'] = name
        if email != '':
            qry = f"UPDATE asp_data SET email = '{email}' WHERE asp_id = '{session['asp_id']}';"
            sql.sql(qry)
            session['asp_email'] = email
        if password != '':
            qry = f"UPDATE asp_data SET password = '{password}' WHERE asp_id = '{session['asp_id']}';"
            sql.sql(qry)
            session['asp_password'] = password
 
        if owner != '':
            qry = f"UPDATE asp_data SET owner = '{owner}' WHERE asp_id = '{session['asp_id']}';"
            sql.sql(qry)
            session['asp_owner'] = owner
 
        if location != '':
            qry = f"UPDATE asp_data SET location = '{location}' WHERE asp_id = '{session['asp_id']}';"
            sql.sql(qry)
            session['asp_location'] = location
 
        if address != '':
            qry = f"UPDATE asp_data SET address = '{address}' WHERE asp_id = '{session['asp_id']}';"
            sql.sql(qry)
            session['asp_address'] = address
 
        return redirect('/asp_profile_edit_request')
    else:
        return render_template('show_message.html', message = 'The session ended Please login again')
    

@asp.route('/asp/receive_car_form')
def receive_car_form():
    if 'asp_id' in session:
        return render_template('asp_rcv_car.html')
    else:
        return redirect('/asp')
    
@asp.route('/rcv_car', methods=['POST'])
def rcv_car():
    if 'asp_id' in session:
        vo_mail = request.form['vo_mail']
        v_id = sql.sql_data(f'select max(v_id) from cars')[0][0]
        if v_id == None:
            v_id = 0
        else:
            v_id = str(int(v_id) + 1)       
        sql.sql(f"INSERT INTO cars (v_id, asp_id, vo_mail) VALUES ('{v_id}','{session['asp_id']}','{vo_mail}')")
        return render_template('message.html',message = 'Vehicle Added to Queue.', href = '/asp/receive_car_form')
    else:
        return redirect('/asp')

@asp.route('/asp/show_regular_req')
def show_regular_req():
    if 'asp_name' in session:
        id = session['asp_id']
        s = sql.sql_dict(f"select request_id, vo_id, service_name, status, time_slot, contact from regular where asp_id = '{id}'")
        return render_template('asp_show_regular_request.html', id = id, cars = s)
    else:
        return redirect('/asp')

@asp.route('/asp_commit_slot' , methods = ['POST'])
def asp_commit_slot():
    if 'asp_name' in session:
        id = session['asp_id']
        request_id = request.form['request_id']
        time = request.form['time']
        contact = request.form['contact']
        qry = f"UPDATE regular set status = 'Accepted', time_slot = '{time}', contact = '{contact}' where request_id = '{request_id}'"
        sql.sql(qry)
        return render_template('message.html',message = 'Request Acceepted', href = '/asp/show_regular_req')

    else:
        return redirect('/asp')