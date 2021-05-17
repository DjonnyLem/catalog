from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from menu import menu
import os
from flask import flash
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
    # for i in el:
        # print('i=', i)
    if request.method == "POST":
        if 'filesize' in request.cookies:
        
            print ('O-OK')
            print('filesize111 =',request.cookies["filesize"])
        else:
            print ('N-NOK')
               
        if request.form["indetify"] == "form1":                 
            past_str = Defect.query.order_by(Defect.id.desc()).first()    #берем из БД последнюю запись, сортированную по убыванию по id
            print ('!!!!',past_str)
            if past_str == None:
                id_name=0
            else:
                id_name=past_str.id
            print ('id_name=',id_name)       
            defect = (request.form['defect']).upper()       #запись с поля name= 'defect'
            image = request.files['image']          #файл из поля name= 'image'
            ff = request.form
            fl = request.files['image']
            filename = secure_filename(image.filename)
            e=fl.filename.rsplit('.',1)
            # s="="*10
            # print('eee=',e)
            # print(defect, image)
            # print ('new=   ',ff)
            # print ('now=   ',fl.filename)
            # print ('id=   ',past_str.id)
            # print ("="*10)
            # print('size=',s)
            path1 = os.getcwd()
            path2= 'static/img/uploads/'

            fl_name=path2+"file_"+str(id_name+1)+"."+e[1]
            #image.save(os.path.join(path1, fl_name))
            print (os.path.join(path1, fl_name))
            q = Defect(defect_name=defect, image=fl_name)
            print(q.image)            
#            return render_template("example_add.html")

                   
            try:
                
                db.session.add(q)
                #db.session.add(defect)
                #db.session.add(image)
                db.session.commit()
                
                image.save(os.path.join(path1, fl_name))
                #flash ('Пароль должен содержать не менее 10 символов')
                #print('Пароль должен содержать не менее 10 символов')
                #b = Defect.query.order_by(Defect.id.desc()).first() 
                #ss = str(b.id)
                
                #sss = b.image.rsplit('/',1)[1].split('.')[0].split('_')[1]
                #print (past_str.id, '->', ss)
                #if ss==sss:
                    #print ('OK')
                    #db.session.commit()
                return redirect('/example_add')

            except:
                return "При добавлении произошла ошибка"

 
    else:
        
        return render_template("example_add.html")

# Функция os.path.exists () принимает аргумент строкового типа, который может быть либо именем каталога, либо файлом.

if __name__ == "__main__":
    app.run(debug=True)
