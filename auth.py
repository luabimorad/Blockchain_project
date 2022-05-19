
from flask import Blueprint,render_template,request,flash, redirect, url_for
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from blockchain import current_blockchain, User as BUser, Transaktion

auth = Blueprint('auth',__name__)   

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name=request.form.get('user_name')
        password = request.form.get('password')
        user = User.query.filter_by(user_name=user_name).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.account'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User Name does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout') 
@login_required 
def logout():
    logout_user()
    flash('Logged out!',category='success')
    return redirect(url_for('auth.login')) 

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
         user_name = request.form.get('user_name')
         first_name = request.form.get('first_name')
         surname = request.form.get('surname')
         email =request.form.get('email')
         LuCoins=int(request.form.get('LuCoins'))
         password1 = request.form.get('password1')
         password2 = request.form.get('password2')

         user = User.query.filter_by(user_name=user_name).first()
         if user:
             flash('User name already exists.', category='error')
         elif  len(user_name) < 2:
             flash('User Name must be greater than 2 characters.', category='error')
         elif len(first_name) < 2:
             flash('First name must be greater than 1 character.', category='error')
         elif first_name == user_name:
             flash('First name and User name must be differents.', category='error')    
         elif len(first_name) < 2:
             flash('Surname must be greater than 1 character.', category='error')
         elif len(email) < 2:
             flash('Email must be greater than 1 character.', category='error')  
         elif "@" not in email:
             flash('Email must be have @.', category='error')   
         elif LuCoins >50 or LuCoins<1:
             flash('You can buy greater than 1 LuCoins or maximal 50', category='error')  
         elif len(password1) < 7:
             flash('Password must\'t be greater than 6 characters.', category='error')                  
         elif password1 != password2:
             flash('Passwords don\'t match.', category='error')
         else:
             new_user = User(user_name=user_name, first_name=first_name,surname=surname,email=email,LuCoins=LuCoins
             , password=generate_password_hash(
                password1, method='sha256'))
             db.session.add(new_user)
             db.session.commit()
             login_user(new_user, remember=True)
             flash('Congratulation,you are a client!The experience begin!', category='success')
             return redirect(url_for('views.home'))

    return render_template("sign_up.html")

@auth.route('/account', methods=['GET', 'POST'])
def buy_sell():
    if "buy" in request.form:
        return buy_coins()
    elif "sell" in request.form:
        return sell_coins()
    else:
        print("Something is wrong")


def buy_coins():
    if request.method == 'POST':
            LuCoins=request.form.get('buy_LuCoins')
            buy_whom = request.form.get('buy_whom')

            if not buy_whom:
                flash("Please enter User Name",category='error')
                return redirect(url_for('views.account'))
            if not LuCoins:
                  flash("Please enter how many Lu Coins do you want to buy",category='error')  
                  return redirect(url_for('views.account'))
            else:
                LuCoins = int(LuCoins)

            db_user = User.query.filter_by(user_name=current_user.user_name).first()
            db_buy_whom = User.query.filter_by(user_name=buy_whom).first()
            if db_user and db_buy_whom:
                    if LuCoins>0 and db_user != db_buy_whom and  db_buy_whom.LuCoins > LuCoins:
                        # Blockchain
                        buser_receiver = BUser(db_user.user_name,db_user.LuCoins)
                        buser_sender = BUser(db_buy_whom.user_name,db_buy_whom.LuCoins)
                        transaction = Transaktion(buser_sender,buser_receiver, LuCoins)
                        current_blockchain.append(transaction)

                        # DB
                        db_user.LuCoins += LuCoins
                        db_buy_whom.LuCoins -= LuCoins
                        db.session.commit()

                        flash("Congratulations! You have bought more coins",category='success')
                    elif  db_user == db_buy_whom:
                        flash("The Current user musn\'t be the same as the user that you buy",category='error')
                    elif db_buy_whom.LuCoins<LuCoins :
                        flash("The user haven\'t enough LuCoins",category='error')
                    elif LuCoins<=0 :
                        flash("You must buy more than 0 LuCoins",category='error')        
                    else:
                        flash("error",category='error')
                        return redirect(url_for('views.account'))
            else:
                 flash('User Name does not exist.', category='error')
  
    
    return(render_template("account.html", user=current_user)) 

   
def sell_coins():
    if request.method == 'POST':
            LuCoins=request.form.get('sell_LuCoins')
            sell_whom = request.form.get('sell_whom')

            if not sell_whom:
                flash("Please enter User Name",category='error')
                return redirect(url_for('views.account'))
            if not LuCoins:
                  flash("Please enter how many Lu Coins do you want to sell",category='error')  
                  return redirect(url_for('views.account'))
            else:
                LuCoins = int(LuCoins)
        
            db_user = User.query.filter_by(user_name=current_user.user_name).first()
            db_sell_whom = User.query.filter_by(user_name=sell_whom).first()
            if db_user and db_sell_whom:
                    if LuCoins>0 and db_user != db_sell_whom and  db_user.LuCoins > LuCoins:
                        # Blockchain
                        buser_sender = BUser(db_user.user_name,db_user.LuCoins)
                        buser_receiver = BUser(db_sell_whom.user_name,db_sell_whom.LuCoins)
                        transaction = Transaktion(buser_sender,buser_receiver, LuCoins)
                        current_blockchain.append(transaction)

                        # DB
                        db_user.LuCoins -= LuCoins
                        db_sell_whom.LuCoins += LuCoins
                        db.session.commit()

                        flash("OK! You have sold coins",category='success')
                    elif  db_user == db_sell_whom:
                          flash("The Current user musn\'t be the same as the user that you sell",category='error')
                    elif db_user.LuCoins<=1 :
                           flash("You don\'t have enough LuCoins",category='error')  
                    elif  LuCoins >= db_user.LuCoins:
                          flash("You must have at least 1 coin in your portfolio",category='error')         
                    else:
                          flash("error",category='error')
            else:
                   flash('User Name does not exist.', category='error')
  
    
    return(render_template("account.html", user=current_user))