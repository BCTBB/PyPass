from flask import Flask, request, url_for, render_template, redirect, flash
from flaskext.mysql import MySQL
from datetime import timedelta, datetime
import random, string
from forms import loginForm

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'mySecretUser'
app.config['MYSQL_DATABASE_PASSWORD'] = '<Password>'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(int(32)))
mysql.init_app(app)

db = mysql.connect()

@app.route('/', methods=["GET", "POST"])
def login():
    form = loginForm()

    if request.method == 'POST':
        if ( form.validate() == False ):
            flash('All fields are required.')
            return render_template('landing.html', **locals())
        else:
            name = request.form.get("name", "")
            return render_template('return.html', **locals())
    elif (request.method == 'GET'):
        return render_template('landing.html', **locals())

@app.route("/code")
def hascode():
    code = request.args.get('Number')

    cursor = db.cursor()
    cursor.execute("SELECT COUNT(userName) from User where code = '" + str(code) + "'")
    codeCount = cursor.fetchone()

    if (codeCount[0] == 0):
        message = "You did not specify a valid Code."
    else:
        cursor.execute("SELECT days from User where code = '" + str(code) + "'")
        codeDays = cursor.fetchone()
        cursor.execute("SELECT date from User where code = '" + str(code) + "'")
        codeDate = cursor.fetchone()
        if ((codeDate[0] + timedelta(days=int(str(codeDays[0])))) < datetime.now()):
            message = "Password has expired & deleted"
            cursor.execute("DELETE FROM User where code = '" + code + "'")
        else:
            cursor.execute("SELECT userName from User where code = '" + str(code) + "'")
            codeUser = cursor.fetchone()
            cursor.execute("SELECT password from User where code = '" + str(code) + "'")
            codePW = cursor.fetchone()
            # cursor.execute("SELECT password from User where code = '" + code + "'")
            passwordExpiration = (codeDate[0] + timedelta(days=int(str(codeDays[0]))))
            todaysDate = datetime.now()

    return render_template(
        'password.html', **locals())

@app.route("/generatepassword")
def generatepw():

    username = request.args.get('UserName')
    passwordLength = request.args.get('PWLength')
    retainDays = request.args.get('retention')

    if (username == '' or not username):
        message = "Specify a Username"

        return render_template(
            'return.html', **locals())

    if (passwordLength is None or passwordLength == ''):
        passwordLength = 10
        pass
    elif (int(passwordLength) > 40 and passwordLength is not None):
        message = "Password is too long"

        return render_template(
            'return.html', **locals())

    cursor = db.cursor()
    cursor.execute("SELECT Password from User where Username = '" + username + "'")
    data = cursor.fetchone()

    if data is None:
        if ( retainDays == '' or retainDays <= 0):
            retainDays = 7

        message = "Your generated password is below"
        N = str(passwordLength)
        randomPassword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(int(N)))
        nowtime = datetime.now()

        # generate a new random code if the code already exists in the database
        randomString = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(int(32)))

        cursor.execute("SELECT COUNT(code) from User where code = '" + str(randomString) + "'")
        codeExists = cursor.fetchone()

        while ( int(codeExists[0]) > 0):
            randomString = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(int(32)))

        cursor.execute("INSERT INTO User (userName, password, code, date, days) VALUES ('" + username + "','" + randomPassword + "','" + randomString + "','" + str(nowtime) + "','" + str(retainDays) + "')")
        db.commit()

        cursor.execute("SELECT days from User where code = '" + str(randomString) + "'")
        codeDays = cursor.fetchone()
        cursor.execute("SELECT date from User where code = '" + str(randomString) + "'")
        codeDate = cursor.fetchone()

        passwordExpiration = (codeDate[0] + timedelta(days=int(str(codeDays[0]))))
        todaysDate = datetime.now()
    else:
        # length = 10
        message = "To view the password that was generated, please use the code that was provided to you"

    return render_template(
        'return.html', **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
