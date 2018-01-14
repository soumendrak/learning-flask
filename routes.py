from flask import Flask, render_template, request
from models import db, User
from forms import SignupForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

app.secret_key = 'development-secret-key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate():
            new_user = User(form.first_name.data, form.last_name.data,
                            form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return 'User signed up successfully'
        else:
            return render_template('signup.html', form=form)
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
