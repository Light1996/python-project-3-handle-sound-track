import pathlib
import logging
from flask import Blueprint, render_template, request, redirect, session
from models import User, TrackRecords
from app import db
import pandas as pd
import os

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

PARENT_PATH = str(pathlib.Path(__file__).parent.resolve())
UPLOAD_FOLDER = PARENT_PATH + '\static'

user_blueprints = Blueprint('user_blueprints', __name__)


def parseCSV(filePath):
    temp = list()

    # CVS Column Names
    col_names = ['Name', 'Year', 'Artist', 'Composer']
    try:
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(filePath, names=col_names, header=None)
        loggedin = session['user']
        user = User.query.filter_by(email=loggedin).first()
        # Loop through the Rows
        for i, row in csvData.iterrows():
            temp.append([i[0], i[1], i[2], i[16]])
            entry = TrackRecords(user_id=user.id, name=i[0], year=i[16], artist=i[1], composer=i[2])
            db.session.add(entry)
            db.session.commit()
    except:
        pass

    return temp
    # print(i, row['Name'], row['Year'], row['Artist'], row['Composer'], )


@user_blueprints.route('/')
@user_blueprints.route('/', methods=['POST', 'GET'])
def home():
    if 'user' not in session:
        return redirect('/signin')


    loggedin = session['user']
    user = User.query.filter_by(email=loggedin).first()
    trackes_record = TrackRecords.query.filter_by(user_id=user.id).all()

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            filenameforlater = file_path
            # set the file path
            uploaded_file.save(file_path)
            loggedin = session['user']
            user = User.query.filter_by(email=loggedin).first()
            user.filename = uploaded_file.filename
            db.session.commit()
            recieveddata = parseCSV(file_path)
        # save the file
        return render_template('index.html', check=1, temp_data=recieveddata, trackes_record=trackes_record)
    return render_template('index.html', check=0, temp_data='', trackes_record=trackes_record)


@user_blueprints.route('/signin')
@user_blueprints.route('/signin', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('your_name')
        password = request.form.get('your_pass')
        if username and password is not None:
            user = User.query.filter_by(email=username).first()
            if user:
                if user.password == password:
                    session['user'] = username
                    return redirect('/')

    return render_template('signin.html')


"""
    This route is for Signup to create new account
"""


@user_blueprints.route('/signup')
@user_blueprints.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        re_password = request.form.get('re_pass')
        if username and password is not None:
            entry = User(username=username, email=email, filename=None, password=password, repassword=re_password)
            db.session.add(entry)
            db.session.commit()
            return redirect('/signin')

    return render_template('signup.html')


@user_blueprints.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/signin')
