from logging import error
from flask import Flask, render_template ,request, redirect, url_for, session, g, flash
import sqlite3



app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'customer.db'
ADMIN_ID = 'ujju97'
ADMIN_PASSWORD = '985679'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
@app.route("/")
def hello():
    return render_template('Home.html')

@app.route("/about")
def harry():
    return render_template('about.html')
@app.route("/login")
def Login():
    return render_template('login.html')

@app.route("/login_pg", methods=['GET', 'POST'])
def login_pg():
    if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM cust_det WHERE Username = ? AND Password = ? AND status=? ", (id, password,"unblocked"))
        user = cursor.fetchone()

        if user:
            session['id'] = id
            return redirect(url_for('cust_ds'))
        else:
            flash('Invalid user ID or password.')
            return redirect(url_for('login_pg'))
    return render_template('User_login.html')


@app.route('/cust_ds', methods=['GET', 'POST'])
def cust_ds():
    if 'id' in session:
        ID = session['id']

        services = []
        sr = []
        error = None
        errorz = None


        conn = get_db()
        cursor = conn.cursor()


        if request.method == 'POST':
            pins = request.form.get('pincode')


            if 'fetch_service' in request.form:
                # Handle fetching services for the second pin code
                if not pins:
                    errorz = "Pin code is required"
                else:
                    query = "SELECT Service FROM Acc_sp WHERE Pincode = ?"
                    cursor.execute(query, (pins,))
                    sr = [row[0] for row in cursor.fetchall()]

                    if not sr:  # Corrected this condition
                        errorz = f"No services available for pin code {pins}"

            if  'update' in request.form:
                srid = request.form.get('srid')
                days1 = request.form.get('days1')
                date4 = request.form.get('date11')
                date5 = request.form.get('date12')
                ser = request.form.get('ser')

                cursor.execute('UPDATE Request SET Duration=?,Date_o=?,Date_e=?,Service=? WHERE Srid = ?',
                               (days1, date4, date5, ser, srid))
                conn.commit()
                flash('Successfully Update service')


        if request.method == 'POST':
            pin = request.form.get('pin')

            days = request.form.get('days')
            service = request.form.get('service')
            date1 = request.form.get('date1')
            date2 = request.form.get('date2')





            if 'fetch' in request.form:
                # Handle fetching services for the pin code
                if not pin:
                    error = "Pin code is required"
                else:
                    query = "SELECT Service FROM Acc_sp WHERE Pincode = ?"
                    cursor.execute(query, (pin,))
                    services = [row[0] for row in cursor.fetchall()]

                    if not services:
                        error = f"No services available for pin code {pin}"







            elif 'book' in request.form:
                # Handle booking logic
                if not service or not days:
                    error = "Please select a service and enter the number of days"

                else:
                    try:


                        cursor.execute(
                            '''INSERT INTO Request (username, Service, Duration , Date_o, Date_e) 
                            VALUES (?, ?, ?,?,?)''', (ID, service, days , date1, date2)
                        )
                        conn.commit()
                        flash('Booking successful!', 'success')
                    except Exception as e:
                        conn.rollback()
                        error = "An error occurred while processing your booking. Please try again."


        if request.method == 'POST' and 'submit' in request.form:
             rv=request.form['review']
             cursor.execute(
                 '''INSERT INTO Review (username, review) 
                 VALUES (?, ?)''', (ID, rv)
             )
             conn.commit()
             flash('Review Submitted!', 'success')


        if request.method == 'POST' and 'close' in request.form:
            srid = request.form.get('srid')

            cursor.execute('UPDATE Request SET Status=? WHERE Srid = ?', ("Close",srid))
            conn.commit()
            flash('Successfully Update service')
        if request.method == 'POST' and 'open' in request.form:
            srid = request.form.get('srid')

            cursor.execute('UPDATE Request SET Status=? WHERE Srid = ?', ("Open",srid))
            conn.commit()
            flash('Successfully Update service')
        if request.method == 'POST' and 'pay' in request.form:
            serid = request.form.get('serid')

            cursor.execute('UPDATE Request SET Payment=? WHERE Srid = ?', ("Paid",serid))
            conn.commit()
            flash('Successfully Paid')

        cursor.execute("SELECT Username,Service, Duration,Date_o,Payment,Date_e,Srid,Status FROM Request WHERE Username=?", (ID,))
        users = cursor.fetchall()

        cursor.execute("SELECT Username,Service, Duration,Date_o,Payment,Date_e,Srid,Status ,prfid FROM Request WHERE Username=? and Ser_st=?",(ID,"Accepted"))
        table = cursor.fetchall()
        conn.close()

        # Render the template with current state
        return render_template('Cust_dash.html', user={'id': id}, services=services,errorz=errorz,error=error,table=table,users=users,sr=sr)
    else:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))




@app.route("/login_pg2", methods=['GET', 'POST'])
def login_pg2():

    if request.method == 'POST':
        userid = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Acc_sp WHERE Username = ? AND Password = ? AND Status = ?", (userid, password , "unblocked"))
        user = cursor.fetchone()

        if user:
            session['userid'] = userid
            return redirect(url_for('sp_dash'))
        else:
            flash('Invalid user ID or password.')
            return redirect(url_for('login_pg'))

    return render_template('sp_login.html')

@app.route("/login_pg3")
def login_pg3():
    return render_template('user_login.html')
@app.route("/Reg_pg2", methods=['GET', 'POST'])
def Reg_pg2():
        if request.method == 'POST':
            # Collect form data
            userid = request.form['username']
            password = request.form['password']
            Fullname = request.form['name']
            Gender = request.form['gender']
            address = request.form['address']
            Pincode = request.form['pincode']
            phone = request.form['phone']
            email = request.form['email']


            # Insert data into the database
            db = get_db()
            cursor = db.cursor()
            cursor.execute('''INSERT INTO cust_det 
                              (Username, Password, Name, Gender, Address, Pincode, Phone, Email) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (userid, password, Fullname,Gender, address, Pincode, phone, email))
            db.commit()
            flash('Registration successful!')
            return redirect(url_for('login_pg3'))
        return render_template('user_reg.html')

@app.route("/Reg_pg", methods=['GET', 'POST'])
def Reg_pg():
    db = get_db()
    cursor = db.cursor()


    query = "SELECT service FROM sr"
    cursor.execute(query)
    service = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':

        userid = request.form['Username']
        password = request.form['pass']
        Fullname = request.form['name']
        Gender = request.form['gender']
        address = request.form['address']
        Pincode = request.form['pincode']
        phone = request.form['phone']
        email = request.form['email']
        exp = request.form['experience']
        services = request.form['services']


        cursor.execute('''INSERT INTO ser_pr 
                              (Username, Password, Full_Name, Gender, Address, Pincode, Phone, Email, Experience, Service_Type) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (userid, password, Fullname, Gender, address, Pincode, phone, email, exp, services))
        db.commit()

        flash('Registration successful!')
        return redirect(url_for('login_pg2'))
    return render_template('Reg_SP.html', service=service)





@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('login_pg'))



@app.route('/sp_dash', methods=['GET', 'POST'])
def sp_dash():
    if 'userid' not in session:
        return redirect('/login')

    ID = session['userid']
    conn = get_db()
    cursor = conn.cursor()


    cursor.execute('SELECT Service, Pincode FROM Acc_sp WHERE Username = ?', (ID,))
    result = cursor.fetchone()
    if not result:
        return "No services found for the logged-in professional."

    Service, Pincode = result
    customer_details = None
    users = []
    table = []
    customer_details=None
    if request.method == 'POST':
        username = request.form.get('username')
        srid = request.form.get('srid')
        if 'Get' in request.form:
            cursor.execute(
                '''
                SELECT  Name, Gender,Address, Pincode, Phone, Email FROM cust_det WHERE Username = ? ''',(username,) )
            customer_details = cursor.fetchone()
            if not customer_details:
                flash('Customer not found')

        if 'accept' in request.form:
            cursor.execute(
                '''
                UPDATE Request SET Ser_st = ? , prfid=? WHERE Srid = ? ''', ( "Accepted",ID,srid))
            conn.commit()

        if 'reject' in request.form:
            cursor.execute(
                '''
                UPDATE Request SET Ser_st = ? , prfid=? WHERE Srid = ? ''', ("Rejected", ID, srid))
            conn.commit()


        if 'close' in request.form:
            cursor.execute(
                '''
                UPDATE Request SET Ser_st = ? , prfid=? WHERE Srid = ? ''', ("Closed", ID, srid))
            conn.commit()

    # Fetch all requests for the current service
    cursor.execute('''SELECT username, Service, Duration, Date_o, Date_e, Payment, Srid ,Ser_st FROM Request WHERE  Status=? and Payment=? ''',("Open","Paid"))
    table = cursor.fetchall()



    conn.close()

    return render_template(
        'SP_dash.html',customer_details=customer_details,users=users,table=table)



@app.route('/login_pg1', methods=['GET', 'POST'])
def login_pg1():
    if request.method == 'POST':
        userid = request.form.get('Username')
        password = request.form.get('Password')


        if userid == ADMIN_ID and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin ID or password.')
            return redirect(url_for('login_pg1'))

    return render_template('Admin_login.html')


# Admin dashboard route (protected)
@app.route('/admin_ds')
def admin_dashboard():
    # Check if the admin is logged in
    if not session.get('admin'):
        return redirect(url_for('login_pg1'))

    return render_template('Admin_dash.html')

# Management system for Admins Dashboard
@app.route('/cust_mnt', methods=['GET', 'POST'])
def cust_mnt():
    conn = sqlite3.connect('customer.db')
    cursor = conn.cursor()

    # Handle "Get Details" form submission
    customer_details = None
    if request.method == 'POST' and 'Get_details' in request.form:
        user_id = request.form.get('username')
        cursor.execute('SELECT Name, Email, Pincode,Phone, status,Address,Gender FROM cust_det WHERE Username = ?', (user_id,))
        customer_details = cursor.fetchone()
        if not customer_details:
            flash('Customer not found')

    # Handle "Block Customer" form submission
    if request.method == 'POST' and 'block_customer' in request.form:
        user_id = request.form.get('username')
        cursor.execute('UPDATE cust_det SET status = "Blocked" WHERE Username = ?', (user_id,))
        conn.commit()
        flash('Customer has been blocked')
    if request.method == 'POST' and 'unblock_customer' in request.form:
        user_id = request.form.get('username')
        cursor.execute('UPDATE cust_det SET status = "unblocked" WHERE Username = ?', (user_id,))
        conn.commit()
        flash('Customer has been unblocked')

    # Fetch list of all users for display in the table
    cursor.execute('SELECT Username, Name, Pincode , status FROM cust_det')
    users = cursor.fetchall()


    cursor.execute('SELECT * FROM Review')
    table = cursor.fetchall()
    conn.close()


    return render_template('Cust_mnt.html', users=users, customer_details=customer_details,table=table)


@app.route('/sp_mnt', methods=['GET', 'POST'])
def sp_mnt():
    conn = sqlite3.connect('customer.db')
    cursor = conn.cursor()
    pr_detail_acc = None

    # Handle "Get Details" form submission
    pr_details = None

    if request.method == 'POST' and 'Get_details' in request.form:
        user_id = request.form.get('username')
        cursor.execute('SELECT Full_Name, Gender, Phone, Status ,Service , Experience , Pincode FROM Acc_sp WHERE Username = ?', (user_id,))
        pr_details = cursor.fetchone()
        if not pr_details:
            flash('Professional not found')


    # Handle "Block Customer" form submission
    if request.method == 'POST' and 'block_professional' in request.form:
        user_id = request.form.get('username')
        cursor.execute('UPDATE Acc_sp SET status = "Blocked" WHERE Username = ?', (user_id,))
        conn.commit()
        flash('Customer has been blocked')
    if request.method == 'POST' and 'unblock_professional' in request.form:
        user_id = request.form.get('username')
        cursor.execute('UPDATE Acc_sp SET status = "unblocked" WHERE Username = ?', (user_id,))
        conn.commit()
        flash('professional has been unblocked')


    if request.method == 'POST' and 'detail' in request.form:
        userid = request.form.get('user')
        cursor.execute('SELECT Full_Name, Gender, Phone, Status ,Service_Type, Address , Experience , Pincode FROM ser_pr WHERE Username = ?',
                       (userid,))
        pr_detail_acc = cursor.fetchone()
        if not pr_detail_acc:
            flash('Professional not found')

    if request.method == 'POST' and 'approve_professional' in request.form:
        user_id = request.form.get('user')
        cursor.execute('INSERT INTO Acc_sp (Username,Password,Gender,Pincode,Phone,Address,Email,Service,Full_name,Experience ) '
                       'SELECT Username,Password,Gender,Pincode,Phone,Address,Email ,Service_Type ,Full_Name,Experience FROM ser_pr WHERE Username = ?', (user_id,))
        cursor.execute('''
                    DELETE FROM ser_pr
                    WHERE Username = ?
                ''', (user_id,))
        conn.commit()

    if request.method == 'POST' and 'reject_professional' in request.form:
        user_id = request.form.get('userid')
        cursor.execute('DELETE FROM ser_pr WHERE Username = ?', (user_id,))
        conn.commit()







    # Fetch list of all users for display in the table
    cursor.execute('SELECT Username , Full_Name ,Gender,Phone,Service_Type ,Address , status FROM ser_pr')
    users = cursor.fetchall()
    cursor.execute('SELECT Username , Full_Name ,Gender,Phone,Service ,Address , status FROM Acc_sp')
    table = cursor.fetchall()

    cursor.execute('SELECT Service, COUNT(*) FROM Acc_sp GROUP BY Service')
    service_data = cursor.fetchall()

    labels = [row[0] for row in service_data]
    counts = [row[1] for row in service_data]

    conn.close()


    return render_template('sp_mnt.html', users=users,table=table, pr_details=pr_details, pr_detail_acc=pr_detail_acc ,labels=labels,counts=counts)




@app.route('/service', methods=['GET', 'POST'])
def service():
    conn = sqlite3.connect('customer.db')
    cursor = conn.cursor()

    if request.method == 'POST' and 'create' in request.form:
        # Collect form data
        ser = request.form['service']
        price = request.form['price']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO sr
                                  (service,price) 
                                  VALUES (?, ?)''',
                       (ser, price))
        db.commit()
        flash('Service Creation successful!')
    if request.method == 'POST' and 'update' in request.form:
        serv = request.form.get('service1')
        rate= request.form.get('price1')
        cursor.execute('UPDATE sr SET price = ? WHERE service = ?', (rate,serv))
        conn.commit()
        flash('Successfully Update service')
    if request.method == 'POST' and 'delete' in request.form:
        serv1 = request.form.get('service2')
        cursor.execute('Delete From sr WHERE service = ?', (serv1,))
        conn.commit()
        flash('Successfully Delete service')

    cursor.execute('SELECT service, price FROM sr')
    table1 = cursor.fetchall()




    return render_template('service.html',table1=table1)

@app.route('/About')
def about():

    return render_template('about.html')




@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()







if __name__ == '__main__':
    app.run(debug=True)

