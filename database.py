import xlrd
import os
import sys
import datetime
import click
import random
import time
import threading
from flask import Flask, render_template,session,redirect,url_for,flash,make_response,request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField,StringField,SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Wenke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paiming = db.Column(db.Integer,default=0)
    name = db.Column(db.String(120))
    toudangrenshu = db.Column(db.Integer,default=0)
    toudangxian = db.Column(db.Integer,default=0)
    toudangmingci = db.Column(db.Integer,default=0)



class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paiming = db.Column(db.Integer,default=0)
    name = db.Column(db.String(120))
    toudangrenshu = db.Column(db.Integer,default=0)
    toudangxian = db.Column(db.Integer,default=0)
    toudangmingci = db.Column(db.Integer,default=0)



workbook = xlrd.open_workbook(r'D:\Python\Python37-32\python_excel\like.xlsx')
sheet2 = workbook.sheet_by_name('Sheet1')
for num1 in range(1257):
    paiming = sheet2.cell(num1,0).value
    name = sheet2.cell(num1,1).value
    toudangrenshu = sheet2.cell(num1,2).value
    toudangxian = sheet2.cell(num1,3).value
    toudangmingci = sheet2.cell(num1,4).value
    newlike = Like(paiming=paiming,name=name,toudangrenshu=toudangrenshu,toudangxian=toudangxian,toudangmingci=toudangmingci)
    db.session.add(newlike)
    db.session.commit()
    print(num1)

print('over')

