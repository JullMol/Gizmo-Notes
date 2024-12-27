from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session
from email_validator import validate_email
from string import punctuation
from .database import Users
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .email_file import send_login_information
from datetime import datetime, timedelta, timezone

auth = Blueprint('auth', __name__)

def clean_session():
    preseverved_key = ['_user_id', '_id']
    data_to_keep = {key: session[key] for key in preseverved_key if key in session}
    session.clear()
    session.update(data_to_keep)

def is_login_info_expired():
    login_info_timestamp = session.get('login_info_timestamp')
    if login_info_timestamp:
        if (datetime.now(timezone.utc) - login_info_timestamp) > timedelta(minutes=30):  # Set your desired expiration time
            clean_session()  # Clear the session if expired
            return True
    return False

def is_emailValid(email):
    try:
        validate_email(email)
        return True
    except Exception as e:
        print(e)
        return False

@auth.route('/')
def auth_page():
    if current_user.is_authenticated:
        print(current_user)
        return render_template('home.html')  # Updated line
    return render_template("auth.html")

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = Users.query.filter_by(email=email).first()
    if user: 
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({
                "success": True, 
                'redirect': url_for('auth.auth_page')
            })
        else:
            return jsonify({
                "success": False, 
                'message': 'Incorrect password, please try again.'
            })
    return jsonify({
        "success": False, 
        'message': 'Email not found'
    })

@auth.route('/signup', methods=['POST'])
def signup():
    # Get the data from the request
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')  # Changed 'name' to 'username' for clarity
    password1 = data.get('password1')
    password2 = data.get('password2')

    # Prepare the response dictionary
    response = {
        "success": False,
        "message": ""  # Changed 'Message' to 'message' for consistency
    }

    # Check if the email is already registered
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        response['message'] = "This email is already registered."
    elif len(username) < 4:
        response['message'] = "Username must be at least 4 characters long."
    elif not is_emailValid(email):
        response['message'] = "Please enter a valid email address."
    elif password1 != password2:
        response['message'] = "Passwords do not match."
    elif len(password1) < 8:
        response['message'] = "Password must be at least 8 characters long."
    else:
        try:
            new_user = Users(
                email=email,
                username=username,
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()

            # Send login information to the user's email
            send_login_information(email, username, password1)

            response["success"] = True
            response["message"] = "Signup successful! Welcome to gizmonotes."
            response["redirect"] = url_for('auth.auth_page')
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            response['message'] = f"Error saving user: {str(e)}"

    return jsonify(response)

@auth.route('/login_confirmation', methods=['POST'])
def login_confirmation():
    email = session.get('email')
    password = session.get('password')
    response = {
        "success": False,
    }

    # Check if the user already exists
    if Users.query.filter_by(email=email).first():
        response['Message'] = "Email sudah terdaftar"
    else:
        # Create a new user
        new_user = Users(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in
        login_user(new_user, remember=True)
        clean_session()
        
        response["success"] = True
        response["redirect"] = url_for('auth.auth_page')  # Redirect to auth or appropriate page

    return jsonify(response)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.auth_page'))