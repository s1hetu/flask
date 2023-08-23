from flask import Blueprint, render_template, request, flash, redirect, url_for
from .forms import LoginForm, RegisterForm, CreateTagForm, AddressForm
from QA import bcrypt, db, login_manager
from .models import User, Tag, Address
from flask_login import login_user, logout_user, current_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/', methods=['GET'])
@user_blueprint.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('user/home.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"{form.username.data} logged in successfully.", 'success')
            return redirect(url_for('user.home'))
        flash(f"{form.username.data} login failed.", 'danger')
    return render_template('user/login.html', form=form)


@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f"{form.username.data} User created successfully.", "success")
            return redirect(url_for('user.login'))
        flash(f"User with that username already exists.", "danger")
    return render_template('user/signup.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user_blueprint.route('/create_tag', methods=['GET', 'POST'])
@login_required
def create_tag():
    form = CreateTagForm()
    if form.validate_on_submit():
        name = form.name.data
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag-{name} created successfully.", 'success')
        return redirect(url_for('user.view_tags'))
    return render_template('user/create_tag.html', form=form)


@user_blueprint.route('/view_tags')
@login_required
def view_tags():
    return render_template('user/view_tags.html', tags=Tag.query.all())


@user_blueprint.route('/my_tags', methods=['GET'])
def get_my_tags():
    return render_template('user/my_tags.html', tags=current_user.tags)


@user_blueprint.route('/add_address', methods=['GET', 'POST'])
def add_address():
    form = AddressForm()
    if current_user.address:
        flash("User has already added the address", "warning")
        return redirect(url_for('user.home'))
    if form.validate_on_submit():
        city = form.city.data
        state = form.state.data
        address = Address(city=city, state=state, user=current_user)
        db.session.add(address)
        db.session.commit()
        flash("Address added successfully", 'success')
        return redirect(url_for('user.home'))
    return render_template('user/address_template.html', form=form)

