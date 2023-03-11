from flask import Flask,render_template,request,redirect,flash
import mariadb
from datetime import datetime

app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
con=mariadb.connect(
    user='root',
    host='localhost',
    password='',
    database='student_management'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/adhome')
def admin_home():
    return render_template('layout2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    cur=con.cursor()
    qry="SELECT * FROM studentform"
    cur.execute(qry)
    res = cur.fetchall()

    return render_template('dashboard.html',getdata = res)

@app.route('/edit/<int:roll_no>',methods=['GET','POST'])
def edit(roll_no):
    
    qry=f"SELECT * FROM studentform WHERE roll_no ={roll_no} "
    cur=con.cursor()
    cur.execute(qry)
    data=cur.fetchall()
    return render_template('editform.html',getdata=data)

@app.route('/update/<int:roll_no>',methods=['GET','POST'])  
def stu_update(roll_no):
    if request.method=='POST':
        name=request.form['name']
        sem=request.form['sem']
        gender=request.form['gender']
        dept=request.form['dept']
        email=request.form['email']
        phone=request.form['phone']
        address=request.form['address']
        
        qry= f"UPDATE studentform SET name='{name}',sem={sem},gender='{gender}',depetment='{dept}',email='{email}',phone_no='{phone}',address='{address}' WHERE roll_no={roll_no}" 
        cur=con.cursor()
        cur.execute(qry)
        con.commit()
        flash(f'{roll_no} ID Student Updated successfully..')
    return render_template('editform.html')


@app.route('/delete/<int:roll_no>',methods=['GET','POST'])
def delete(roll_no):
    qry=f"DELETE FROM studentform WHERE roll_no={roll_no}"
    cur=con.cursor()
    cur.execute(qry)
    con.commit()
    flash(f'{roll_no} ID Student has been Deleted Successfully..')
    return redirect('/dashboard')

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == 'POST':
        getroll = int(request.form.get('roll'))
        q =f"SELECT * FROM studentform WHERE roll_no={getroll}"
        cur = con.cursor()
        cur.execute(q)
        details = cur.fetchall()
        print(details)
        return render_template('search.html',details =  details)
    return render_template('search.html')
            
@app.route('/login',methods=['GET','POST'])   
def login():
  
        if request.method=='GET':
            return render_template('login.html')
   
        else:
            user=request.form['user']
            passw=request.form['password']

        qry= f"SELECT * FROM login WHERE password={passw} AND user_name = '{user}'"
        cur =   con.cursor()
        cur.execute(qry)
        res = cur.fetchall()
        if res:
            return render_template('layout2.html')
        else:
             return redirect('/login')  

@app.route('/logout')
def logout():
    return render_template('login.html')
        
@app.route('/attend',methods=['GET','POST'])
def attendence_form():
    if request.method == 'POST':
        roll=request.form['roll']
        name=request.form['name']
        percent=request.form['percent']
        cur=con.cursor()
        qry="INSERT INTO attendance (roll_no,name,percentage) VALUES(%s,%s,%s)"
        data=roll,name,percent
        cur.execute(qry,data)
        con.commit()
        flash(f'{roll} ID Student Attendance Added Successfully...')
    return render_template('attendance.html')

@app.route('/sform',methods=['GET','POST'])
def student_form():
    if request.method=='POST':
        name=request.form['name']
        sem=request.form['sem']
        gender=request.form['gender']
        dept=request.form['dept']
        email=request.form['email']
        phone=request.form['phone']
        address=request.form['address']
        date=datetime.now()
        cur=con.cursor()
        qry="INSERT INTO studentform (name,sem,gender,depetment,email,phone_no,address,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        data=name,sem,gender,dept,email,phone,address,date
        cur.execute(qry,data)
        con.commit()
        flash('Student added successfully..')

    return render_template('studentform.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        msg=request.form['message']
        date=datetime.now()
        cur=con.cursor()
        qry="INSERT INTO contact (name,email,phone,msg,date) VALUES(%s,%s,%s,%s,%s)"
        data=name,email,phone,msg,date
        cur.execute(qry,data)
        con.commit()
        flash('Message send Successfully..')
    
    return render_template('contact.html')

if __name__=='__main__':
    app.run(debug=True)
