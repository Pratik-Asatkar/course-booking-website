from datetime import timedelta

from flask import Flask, redirect, url_for, render_template, request
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

import models.user as user_db
import config.secrets as secrets
import tools.utils as utils

from controllers.auth_controller import auth

app = Flask(__name__)
app.secret_key = secrets.APP_SECRET
app.config['JWT_SECRET_KEY'] = secrets.JWT_SECRET
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)


jwt = JWTManager(app)


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for('auth.login'))


@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return redirect(url_for('auth.login'))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/profile')
@jwt_required(locations='cookies')
def profile():
    user = get_jwt_identity()
    user_data = user_db.get_info(user['sub'])

    if not user_data['formFilled']:
        return redirect('/form')
    else:
        return render_template('profile.html', user=user_data)


@app.route('/form', methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def form():
    user = get_jwt_identity()
    user_data = user_db.get_info(user['sub'])
    
    if request.method == "GET":
        if user_data['formFilled']:
            return redirect('/profile')
        else:
            return render_template('form.html', user=user_data)
    elif request.method == "POST":
        data = {
            "name": user_data['name'],
            "email": user_data['email'],
            "dob": request.form.get('dob'),
            "address": request.form.get('address'),
            "gender": request.form.get('gender'),
            "course":request.form.get('course'),
        }

        utils.save_response(data)
        user_db.update_form(user['sub'])

        return redirect('/profile')


app.register_blueprint(auth, url_prefix='/auth')


if __name__ == "__main__":
    app.run(debug=True)
