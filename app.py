from os import error
import re
from flask import Flask, render_template, request,redirect,url_for,session
import pyodbc


server = 'tcp:adbsaahilserver.database.windows.net'
database = 'sqldatabase1'
username = 'serveradmin'
password = 'Spa12345'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/main', methods=["POST", "GET"])
def main():
    if request.method == "POST":
            if request.form.get("lbutton"):
                user = session['username']
                question = request.form["questxt"]
                
                cursor = cnxn.cursor()
                cursor.execute("insert into qna (teacher,questions) values ('"+user+"','"+question+"')")
                cnxn.commit()
                    
                    
                return redirect('/main')

            else:
                
                return render_template('main.html')

    if request.method == "GET": 

        if 'username' in session:
            user = session['username']

            cursor = cnxn.cursor()
            cursor.execute("select teacher, questions from qna where answers is null;")
            table = cursor.fetchall()
            return render_template('main.html' ,user=user,rows=table,item1="Teacher's name",item2='Questions')

        
        else:
                
           return render_template('login.html')


@app.route('/update/<string:id_data>', methods = ['GET','POST'])

def grade(id_data):
    if request.method == "POST":
        if request.form.get("gradebutton"):
            user = session['username']
            dop = request.form["dropup"]

            cursor = cnxn.cursor()
            cursor.execute("UPDATE qna SET grades = '"+dop+"' WHERE id = '"+id_data+"';")
            cnxn.commit()
            return redirect('/gradestudent')
        else:
            return redirect('/gradestudent')

    else:
        if 'username' in session:
            user = session['username']

            cursor = cnxn.cursor()
            cursor.execute("select questions,answers,student from qna where id = '"+id_data+"'")
            one = cursor.fetchone()
            return render_template('grade.html',ques=one[0],answser=one[1],user=user,id=id_data,stud=one[2])
        else:
            return render_template('login.html')

@app.route('/gradestudent', methods=["POST", "GET"])
def gradestudent():
                
    if request.method == "GET": 

        if 'username' in session:
            user = session['username']

            cursor = cnxn.cursor()
            cursor.execute("select * from qna where answers is not null;")
            table = cursor.fetchall()
            if table == []:
                err = "NO STUDENT ANSWERED YET"
            else:
                err =""
            print(str(table).count)
            return render_template('gradestudent.html' ,user=user,rows=table,item1="Teacher's name",item2='Question',item3='Answers',item4='Student name',item5='GRADES',item6='ACTION',err=err)

        
        else:
                
           return render_template('login.html')


@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
            if request.form.get("lbutton"):
                uname = request.form["uname"]
                session['username'] = uname
                return redirect('/main')
                
    else: 
        return render_template('login.html')

@app.route('/logout', methods=["POST", "GET"])
def logout():

    session.pop('username', None)

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug =True, host='0.0.0.0')