from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm
from tools import login_required, login_not_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/learningflask'
db.init_app(app)

app.secret_key = 'development-secret-key'


@app.route('/')
@login_not_required
def index():
    return render_template('index.html')


@app.route('/about')
@login_not_required
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
@login_not_required
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate():
            new_user = User(form.first_name.data, form.last_name.data,
                            form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            session['email'] = new_user.email
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', form=form)
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = AddressForm()
    places, lat_lon = [], (12.836649, 77.655809)
    if request.method == 'POST':
        if not form.validate():
            return render_template('home.html', form=form)
        else:
            address = form.address.data
            p = Place()
            fetched_lat_lon = p.address_to_latlng(address)
            
            if any(lat_lon):
                places = p.query(address)
                return render_template('home.html', form=form, my_coordinates=fetched_lat_lon, places=places)
            else:
                return render_template('home.html', form=form)
                

    elif request.method == 'GET':
        return render_template('home.html', form=form, my_coordinates=lat_lon, places=places)


@app.route('/login', methods=['GET', 'POST'])
@login_not_required
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
