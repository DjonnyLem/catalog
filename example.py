from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from menu import menu
import os
from werkzeug.utils import secure_filename  # к обработке фото

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class Example(db.Model):
    __tablename__ = 'example'
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.Unicode)

class Defect(db.Model):
    __tablename__ = 'defect'
    id = db.Column('id', db.Integer, primary_key=True)
    defect_name = db.Column(db.String(30))
    image = db.Column( db.String(30))
    
@app.route('/')
@app.route('/home')
def index():  
    return render_template("example_base1.html")


@app.route('/example_add', methods=['POST', 'GET'])
def add():
    el = request.form
    for i in el:
        print('i=', i)
    if request.method == "POST":
        
        if request.form["indetify"] == "form1":
            past_str = Defect.query.order_by(Defect.id.desc()).first()    
            defect = (request.form['defect']).upper()
            image = request.files['image']  
            ff = request.form
            fl = request.files['image']
            filename = secure_filename(image.filename)
            e=fl.filename.rsplit('.',1)
            s="="*10
            print('eee=',e)
            print(defect, image)
            print ('new=   ',ff)
            print ('now=   ',fl.filename)
            print ('id=   ',past_str.id)
            print ("="*10)
            print('size=',s)
            path= 'static/img/uploads/'
            fl_name=path+"file_"+str(past_str.id+1)+"."+e[1]
            q = Defect(defect_name=defect, image=fl_name)
            print(q.image)            
#            return render_template("example_add.html")
                   
            try:
                
                db.session.add(q)
                #db.session.add(defect)
                #db.session.add(image)
                db.session.commit()
                return redirect('/example_add')
            except:
                return "При добавлении произошла ошибка"

 
    else:
        return render_template("example_add.html")



if __name__ == "__main__":
    app.run(debug=True)
