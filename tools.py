from functools import wraps
from flask import request, redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def login_not_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
