from flask import Flask, render_template, redirect, url_for,flash , session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_login import login_required,logout_user,current_user,login_user,LoginManager, UserMixin
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/prachiti/Desktop/proj/customer_analysis-master/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager= LoginManager()
login_manager.init_app(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'parkar123'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('signup'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if user.password==form.password.data:
				return redirect(url_for('dashboard'))

		return '<h1>Invalid username or password</h1>'
	return render_template('login.html',form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
        

    return render_template('signup.html', form=form)

@app.route('/dashboard')

def dashboard():
    flash ('Customer details')
    cur = mysql.connection.cursor()
    cur.execute("select * from dashboard order by ID")
    data= cur.fetchall()

    return render_template('dashboard.html',data=data)

@app.route('/profit')

def profit():
    flash ('Profit till date')
    cur = mysql.connection.cursor()
    cur.execute("select ID,CUSTOMER_NAME,PRODUCT_NAME,PROFIT_PERCENTAGE FROM dashboard order by PROFIT_PERCENTAGE")
    data = cur.fetchall()

    return render_template('profit.html',data=data)

@app.route('/bestcustomer')
def bestcustomer():
    cur = mysql.connection.cursor()
    cur.execute("select * from v1")
    data = cur.fetchone()
    return render_template('bestcustomer.html',data=data)



@app.route('/bestproduct')
def bestproduct():
    flash ('Best Product')
    cur = mysql.connection.cursor()
    cur.execute("select PRODUCT_NAME,PROFIT_PERCENTAGE FROM dashboard WHERE PROFIT_PERCENTAGE >= ALL (SELECT PROFIT_PERCENTAGE FROM dashboard group by PRODUCT_NAME,PROFIT_PERCENTAGE) GROUP BY PRODUCT_NAME,PROFIT_PERCENTAGE")
    data=cur.fetchone()

    return render_template('bestproduct.html',data=data)


@app.route('/logout')
def logout():
    logout_user()
    flash ('You have now logged out')
    return redirect(url_for('login'))
#use url_for for dashboard and redirect it here

@app.route('/graphs')
def graphs():
    
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')
    plt.show()

    return "graphs"



if __name__ == '__main__':
    app.run(debug=True)