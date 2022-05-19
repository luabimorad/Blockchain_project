#1. log view
from flask import Blueprint,render_template
from flask_login import login_required,current_user

from website.models import User

views = Blueprint('views',__name__)    

@views.route('/')
@views.route('/home')

def home():
    return render_template("home.html")


@views.route('/account')
@login_required
def account():
    user = User.query.filter_by(user_name=current_user.user_name).first()
    return render_template("account.html", user=user)
