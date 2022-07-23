from threading import Thread
from flask import render_template, redirect, url_for, flash, request, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, ChangePasswordForm, AmazonQueryForm, EbayQueryForm, EmailForm, \
    ResetPasswordForm, UserSettings
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
from engine import run_query
from app import app, login_manager
from db_classes import db, User, Query, Product, QuerySettings
from tokenizer import confirm_token, generate_confirmation_token
from mail import send_confirm_email
import pandas as pd
from io import BytesIO
import multiprocessing
import psutil

threads = {}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(email=form.email.data).first()
        if not user_exists:
            if form.email.data == 'my_email@gmail.com':
                is_admin = True
            else:
                is_admin = False
            if form.password.data != form.confirm_password.data:
                flash("Passwords do not match, please try again.",
                      category="error")
                return redirect(url_for('sign_up'))
            else:
                hashed_and_salted_password = generate_password_hash(request.form.get('password'),
                                                                    method='pbkdf2:sha256',
                                                                    salt_length=8)
                user_to_add = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=hashed_and_salted_password,
                    plan=form.plan.data,
                    register_date=datetime.today(),
                    is_confirmed=False,
                    queries=[],
                    is_admin=is_admin
                )
                db.session.add(user_to_add)
                db.session.commit()
                token = generate_confirmation_token(user_to_add.email)
                confirm_url = url_for('confirm_email', token=token, _external=True)
                html = render_template('activate.html', confirm_url=confirm_url)
                send_confirm_email(user_to_add.id, template=html)
                flash("Confirmation email sent successfully, please confirm your email before logging in",
                      category="message")
                return redirect(url_for('login'))
        else:
            flash("You've already signed up with that email, log in instead", category="message")
            return redirect('login')
    return render_template("sign_up.html", form=form)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'message')
    else:
        user.is_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'message')
    return redirect(url_for('login'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_confirmation_token(user.email)
            reset_url = url_for('reset_password', token=token, _external=True)
            html = render_template('reset_password.html', reset_url=reset_url)
            send_confirm_email(user.id, template=html)
            flash("Password reset email sent successfully, check your inbox for instructions")
        else:
            flash("That email does not exist. Please try again", category="error")
    return render_template('forgot_password.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
    if form.validate_on_submit():
        if form.confirm_password.data == form.new_password.data:
            new_hashed_and_salted_password = generate_password_hash(request.form.get('new_password'),
                                                                    method='pbkdf2:sha256',
                                                                    salt_length=8)
            user_to_change = db.session.query(User).filter_by(email=email).first()
            user_to_change.password = new_hashed_and_salted_password
            db.session.commit()
            flash('Password changed successfully, please login with the new password')
            return redirect(url_for('login'))
    return render_template('reset_password_page.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(pwhash=current_user.password, password=request.form.get("old_password")):
            if form.confirm_password.data == form.new_password.data:
                new_hashed_and_salted_password = generate_password_hash(request.form.get('new_password'),
                                                                        method='pbkdf2:sha256',
                                                                        salt_length=8)
                user_to_change = db.session.query(User).filter_by(id=current_user.id).first()
                user_to_change.password = new_hashed_and_salted_password
                db.session.add(user_to_change)
                db.session.commit()
                logout_user()
                flash("Successfully changed password, please re-login")
                return redirect('login')
            flash("Passwords do not match, please try again.", category="error")
            return redirect('change_password')
        flash("Old password incorrect, please try again", category="error")
        return redirect('change_password')
    return render_template('change_password.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        requesting_user = db.session.query(User).filter_by(email=form.get('email')).first()
        if requesting_user != None:
            if requesting_user.is_confirmed:
                if check_password_hash(pwhash=requesting_user.password, password=form.get("password")):
                    login_user(requesting_user)
                    return redirect('/dashboard')
                else:
                    flash("Password incorrect, please try again", category="error")
                    return redirect('login')
            else:
                flash("You must confirm your email before you can access the application.", category="error")
        else:
            flash("That email does not exist. Please try again", category="error")
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/query/<string:type>', methods=['GET', 'POST'])
@login_required
def query(type):
    if type == 'amazon':
        form = AmazonQueryForm()
        if form.validate_on_submit():
            if (form.url.data.startswith("https://amzn.com/") or form.url.data.startswith("https://www.amazon.com/")):
                q = Query(
                    executed_by=current_user,
                    start_time=datetime.utcnow(),
                    ebay_url=form.url.data,
                    type="amazon",
                    products=[]
                )
                flash(
                    "Searching all across the universe...no need to wait, we know you're a busy person, we will e-mail you once the search is done.")
                db.session.add(q)
                db.session.commit()
                thread = Thread(target=run_query, kwargs={'query_id': q.id})
                thread.start()
                return redirect('query')
            else:
                flash("Invalid URL, URL must belong to Amazon domain only.", category="error")
    else:
        form = EbayQueryForm()
        if request.method == "POST":
            # if form.validate_on_submit():
            if (form.url.data.startswith("https://www.ebay.com")):
                num_of_ebay_items = form.num_of_ebay_items.data
                num_of_seller_top_selling = form.num_of_seller_top_selling.data
                if num_of_ebay_items == "All":
                    num_of_ebay_items = 100
                if num_of_seller_top_selling == "All":
                    num_of_seller_top_selling = 50
                q = Query(
                    executed_by=current_user,
                    start_time=datetime.utcnow(),
                    ebay_url=form.url.data,
                    type="ebay",
                    products=[],
                    settings=QuerySettings(num_of_ebay_items=num_of_ebay_items,
                                           num_of_seller_top_selling=num_of_seller_top_selling,
                                           num_of_days_of_recent_sales=form.num_of_days_of_recent_sales.data,
                                           num_of_days_of_most_recent_sales=form.num_of_days_of_most_recent_sales.data,
                                           num_of_sales_in_recent_days=form.num_of_sales_in_recent_days.data,
                                           num_of_sales_in_most_recent_days=form.num_of_sales_in_most_recent_days.data)
                )
                flash(
                    "Searching all across the universe...no need to wait, we know you're a busy person, we will e-mail you once the search is done.")
                db.session.add(q)
                db.session.commit()
                process = multiprocessing.Process(target=run_query, kwargs={'query_id': q.id}, daemon=True)
                threads[q.id] = process
                process.start()
                return redirect('query')
            # else:
            #     flash("Invalid URL, URL must belong to eBay domain only.", category="error")
    return render_template('query.html', type=type, form=form)


@app.route('/query_result/<uuid:query_id>')
@login_required
def query_result(query_id):
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(query_id=query_id).paginate(page=page, per_page=15)
    return render_template('query_result.html', products=products, query_id=query_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/delete/<query_id>')
@login_required
def delete(query_id):
    products = Product.query.filter_by(query_id=query_id).all()
    for product in products:
        db.session.delete(product)
    settings = QuerySettings.query.filter_by(query_id=query_id).first_or_404()
    db.session.delete(settings)
    query = Query.query.filter_by(id=query_id).first_or_404()
    db.session.delete(query)
    db.session.commit()
    flash("Query deleted successfully")
    return redirect(url_for('dashboard'))


@app.route('/stop/<uuid:query_id>')
@login_required
def stop_query(query_id):
    query = Query.query.filter_by(id=query_id).first_or_404()
    query.end_time = datetime.utcnow()
    query.status = "Stopped"
    try:
        parent_pid = threads[query_id].pid
    except KeyError:
        db.session.commit()
        flash("Query is not currently running, successfully marked as stop anyway.")
        return redirect(url_for('dashboard'))
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):
        try:
            child.kill()
        except psutil.NoSuchProcess:
            continue
    parent.kill()
    db.session.commit()
    flash("Query stopped successfully")
    return redirect(url_for('dashboard'))


@app.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = UserSettings(email_notifications=current_user.email_notifications)
    if form.validate_on_submit():
        if request.form.get("email_notifications"):
            current_user.email_notifications = True
        else:
            current_user.email_notifications = False
        db.session.commit()
        flash("Settings saved successfully")
        return redirect(url_for('user_settings'))
    return render_template('user_settings.html', form=form)


@app.route('/new_query')
@login_required
def new_query():
    return render_template('new_query.html')


@app.route('/query_result/<uuid:query_id>/download')
@login_required
def download_result(query_id):
    start_time = Query.query.filter_by(id=query_id).first().start_time.strftime("%d/%m/%Y %H:%M:%S")
    products = Product.query.filter_by(query_id=query_id).all()
    products_dict = {'Amazon Title': [product.amazon_title for product in products],
                     'ASIN': [product.asin for product in products],
                     'eBay Title': [product.ebay_title for product in products],
                     'eBay URL': [product.ebay_url for product in products],
                     'Lifetime Sales': [product.lifetime_sales for product in products],
                     'Recent Sales': [product.recent_sales for product in products]
                     }
    df = pd.DataFrame(products_dict)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, startrow=0, merge_cells=False, sheet_name="Query_Results")
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename=f"eLocator-Query-Result-{start_time}.xlsx", as_attachment=True)


if __name__ == "__main__":
    app.run()
