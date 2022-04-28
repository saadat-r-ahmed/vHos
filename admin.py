from email.headerregistry import Address
from flask import Blueprint, render_template, request, redirect, session
admin = Blueprint("admin", __name__, static_folder = "static", template_folder = "templates")
import sql, hashlib
import datetime, json
from termcolor import colored



@admin.route('/authenticate_admin', methods = ['POST'])
def authenticate_admin():
    if request.method == "POST":
        admin_id = request.form["id"]
        password = request.form["pass"]
        dbpass = sql.sql_data(f"select password from admin_data where admin_id = '{admin_id}';")
        hash = hashlib.md5(password.encode()).hexdigest()


        if len(dbpass) == 0:
            return render_template('message.html',message = 'Login Failed', href = '/admin')

        elif dbpass[0][0] == hash and len(dbpass) == 1:
            session['admin_id'], session['admin_password'], session['admin_name'], session['admin_email'] = sql.sql_data(f"select * from admin_data where admin_id = '{admin_id}'")[0]
            id = session['admin_id']
            name = session['admin_name']

            print(colored(f'\n>>Admin Login [{datetime.datetime.now()}]  {id} - {name}<<\n', 'blue'))
            return redirect('admin_dashboard')

        else:
            return render_template('message.html',message = 'Login Failed', href = '/admin')



@admin.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        id = session['admin_id']
        name = session['admin_name']
        return render_template('admin_dashboard.html', id = id, name = name)
    else:
        return redirect('login_admin')



@admin.route('/admin_logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_password', None)
    session.pop('admin_name', None)
    session.pop('admin_email', None)
    return redirect('login_admin')






@admin.route('/admin_dashboard/show_all_asp')
def show_all_asp():
    if 'admin_id' in session:   
        asps = sql.sql_dict('select * from asp_data')
        return render_template('show_all_asp.html', asps = asps)
    else:
        return redirect('/admin')



# * Statu OOOKKK ✅

@admin.route('/delete_asp', methods = ['POST'])
def delete_asp():
    if 'admin_id' in session:
        name = request.form['asp_id']
        print(name)
        sql.del_asp_db(name)
        return redirect('admin_dashboard')
    else:
        return redirect('/admin')

@admin.route('/update_asp', methods = ['POST'])
def update_asp():
    pk = request.form['pk']    
    name = request.form['name']
    value = request.form['value']
    print(pk, name, value)
    match name:
        case 'name':
            q = f"Update asp_data set name = '{value}' where asp_id = '{pk}'"
        case 'owner':
            q = f"Update asp_data set owner = '{value}' where asp_id = '{pk}'"
        case 'location':
             q = f"Update asp_data set location = '{value}' where asp_id = '{pk}'"
        case 'address':
             q = f"Update asp_data set address = '{value}' where asp_id = '{pk}'"
        case 'email':
             q = f"Update asp_data set email = '{value}' where asp_id = '{pk}'"
        case 'password':
             q = f"Update asp_data set password = '{value}' where asp_id = '{pk}'"
    sql.sql(q)
    return json.dumps({'status':'OK'})




@admin.route('/admin_dashboard/show_all_vo')
def show_all_vo():
    if 'admin_id' in session:   
        vos = sql.sql_dict('select * from owner')
        print(vos)
        return render_template('admin_show_all_vo.html', vos = vos)
    else:
        return redirect('/admin')


@admin.route('/update_vo', methods = ['POST'])
def update_vo():
    pk = request.form['pk']    
    name = request.form['name']
    value = request.form['value']
    print(pk, name, value)
    match name:
        case 'name':
            q = f"Update owner set name = '{value}' where email = '{pk}'"
        case 'longitude':
            q = f"Update owner set longitude = '{value}' where email = '{pk}'"
        case 'latitude':
             q = f"Update owner set latitude = '{value}' where email = '{pk}'"
        case 'password':
             q = f"Update owner set password = '{value}' where email = '{pk}'"

    sql.sql(q)
    return json.dumps({'status':'OK'})

@admin.route('/delete_vo', methods = ['POST'])
def delete_vo():
    if 'admin_id' in session:
        name = request.form['email']
        sql.del_vo_db(name)
        return redirect('/admin_dashboard/show_all_vo')
    else:
        return redirect('/admin')
    

