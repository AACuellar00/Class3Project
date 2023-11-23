from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_data = request.form
        return render_template('forecast.html', form_data=form_data)
    return render_template("home.html")


@views.route('/forecast', methods=['POST'])
def forecast():
    form_data = request.form
    return render_template('forecast.html', form_data=form_data)
