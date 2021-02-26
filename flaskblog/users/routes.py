from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                    RequestResetForm, ResetPasswordForm)
from flaskblog.posts.forms import PostForm
from flaskblog.users.utils import save_picture, send_reset_email



# 'users': the name of blueprint .
users = Blueprint('users', __name__)

# methods : to accept the type of these methods .
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # main.home : main is mean blueprint main
        return redirect(url_for('main.home'))



    form = RegistrationForm() 
    if form.validate_on_submit():
        
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
             password=hash_password)
        db.session.add(user)
        db.session.commit()
        # f: it mean format like example below but that use with python 3.6 and above
        # name = form.username.data
        # flash('Account is created for {} !'.format(name),'success')
        # ---------------------------------
        # success: the flash has a message here, i want to be able to tell me diiference 
        # between the different kinds of alerts so bootstrap has different alert style
        #  for successes and warning and errors the fask function accerpts a second 
        #  argument that is called a ('category') so im gonna pass in the name of the bootstrap 
        #  class that i want this alert to have and that is success
        # note we can pass anything 'success' ,'danger' , 'anything','.....',.... 
        #flash(f'Your Account has been created !, you are now able to log in', 'success')
        flash("your account has been creates! You are now able to log in", 'success')
        # the home is name of function not the page.
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title = 'Register', form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user : not none
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login this user, the function takes remember as argument that gonna be true/false
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #  ternary conditional
            # value11(true) if condition else value2(flase)
            return redirect('next_page')  if next_page else redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessfully, please check email And Password' ,'danger')     

    return render_template('login.html',title='Login', form=form)


        # if form.email.data == 'hanger.zy@hotmail.com' and form.password.data == '123123123':
        #     flash('You Have Been Loged in', 'success')
        #     return redirect(url_for('home'))
        # else:
        #     flash('Login Unsuccessfully, please check Username And Password' ,'danger')
    # return render_template('login.html',title = 'Login', form = form)

@users.route('/logout')
def logout():
    #  don't take any argument cuz it knows what user is logged in
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
# @login_required : to update account will be a route that requires user to be login
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        # current_user.picture = form.picture.data
        db.session.commit()
        flash('Your Account Has Been Updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/post/new', methods=['GET', 'POST'])
# @login_required : to creating new post will be a route that requires user to be login
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', 'sucess')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legand='New Post')


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)