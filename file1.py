from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ede080d803e9f6d30ce3348400e0b49b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
    
  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@app.route("/")
def hello_world():
    return "<p> Hello SEOTech developer </p>"

@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        bcrypt.check_password_hash(pw_hash, form.password.data) # returns True
        user = User(username=form.username.data, email=form.email.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
  
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")