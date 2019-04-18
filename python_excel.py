import xlrd
import os
import sys
import click
from flask import Flask, render_template,session,redirect,url_for,flash,make_response,request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,IntegerField,MultipleFileField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from wtforms import ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
basedir = os.path.abspath(os.path.dirname(__file__))

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

class ToudangForm(FlaskForm):
    x = StringField('输入考生名次', validators=[DataRequired()])
    submit = SubmitField('搜索')

class SchoolForm(FlaskForm):
    x = StringField('输入学校名称', validators=[DataRequired()])
    submit = SubmitField('搜索')

class UploadForm(FlaskForm):
    photo = MultipleFileField('上传图片为png格式，图片名为学校名称。例：吉林农业大学.png', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()

class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('上传图片为png格式，图片名为学校名称。例：吉林农业大学.png', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()

app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'static/')

app.config['ALLOWED_EXTENSIONS'] = ['png']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
#文科
@app.route('/wen/multi-upload', methods=['GET', 'POST'])
def wen_multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        #检查文件是否存在
        if 'photo' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('photo'):
            #检查文件类型
            if f and allowed_file(f.filename):
                filename = f.filename
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename ))
                filenames.append(filename)
            else:
                flash('Invalid file type:')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames'] = filenames
    return render_template('wen_upload.html', form=form)

@app.route('/wen',methods=['GET', 'POST'])
def wen_index():
    datas = Wenke.query.all()
    return render_template('basewen.html',datas=datas)

@app.route('/wen/school',methods=['GET', 'POST'])
def wen_school():
    form = SchoolForm()
    if form.validate_on_submit():
        school_name = form.x.data
        school_name = Wenke.query.filter_by(name=school_name).first()
        return redirect(url_for('wen_specific_school',school_name=school_name.id))
    return render_template('wen_home.html',form=form)

@app.route('/wen/school/<int:school_name>',methods=['GET', 'POST'])
def wen_specific_school(school_name):
    specific_school_name = Wenke.query.filter_by(id=school_name).first()
    return render_template('wen_specific_school.html',specific_school_name=specific_school_name)

@app.route('/wen/toudang',methods=['GET', 'POST'])
def wen_toudang():
    form = ToudangForm()
    if form.validate_on_submit():
        number = form.x.data
        return redirect(url_for('wen_kspaiming',number=int(number)))
    return render_template('wen_home.html',form=form)

@app.route('/wen/toudang/<int:number>',methods=['GET', 'POST'])
def wen_kspaiming(number):
    filters = {
     Wenke.toudangmingci > number-6000,
     Wenke.toudangmingci < number+6000}
    historys = Wenke.query.filter(*filters).all()
    return render_template('wen_kspaiming.html',historys=historys)

#理科
#
@app.route('/li/multi-upload', methods=['GET', 'POST'])
def li_multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        #检查文件是否存在
        if 'photo' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('photo'):
            #检查文件类型
            if f and allowed_file(f.filename):
                filename = f.filename
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename ))
                filenames.append(filename)
            else:
                flash('Invalid file type:')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames'] = filenames
    return render_template('li_upload.html', form=form)
@app.route('/li',methods=['GET', 'POST'])
def li_index():
    datas = Like.query.all()
    return render_template('baseli.html',datas=datas)

@app.route('/li/school',methods=['GET', 'POST'])
def li_school():
    form = SchoolForm()
    if form.validate_on_submit():
        school_name = form.x.data
        school_name = Like.query.filter_by(name=school_name).first()
        return redirect(url_for('li_specific_school',school_name=school_name.id))
    return render_template('li_home.html',form=form)

@app.route('/li/school/<int:school_name>',methods=['GET', 'POST'])
def li_specific_school(school_name):
    specific_school_name = Like.query.filter_by(id=school_name).first()
    return render_template('li_specific_school.html',specific_school_name=specific_school_name)

@app.route('/li/toudang',methods=['GET', 'POST'])
def li_toudang():
    form = ToudangForm()
    if form.validate_on_submit():
        number = form.x.data
        return redirect(url_for('li_kspaiming',number=int(number)))
    return render_template('li_home.html',form=form)

@app.route('/li/toudang/<int:number>',methods=['GET', 'POST'])
def li_kspaiming(number):
    filters = {
     Like.toudangmingci > number-2500,
     Like.toudangmingci < number+2500}
    historys = Like.query.filter(*filters).all()
    return render_template('li_kspaiming.html',historys=historys)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
