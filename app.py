from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import random
app = Flask(__name__)
app.secret_key='some secret key'


#Config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='bloodbank'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#init MySQL
mysql =  MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1,max=25)])
    email = StringField('Email',[validators.Length(min=10,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method  == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        e_id = name+str(random.randint(1111,9999))
        #Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO RECEPTION(E_ID,NAME,EMAIL,PASSWORD) VALUES(%s, %s, %s, %s)",(e_id, name, email, password))
        #Commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flashing_message = "Success! You can log in with Employee ID " + str(e_id)
        flash( flashing_message,"success")

        return redirect(url_for('register'))

    return render_template('register.html',form = form)

if __name__ == '__main__':
    app.run(debug=True)
