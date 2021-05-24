from flask import Flask, render_template, url_for, request, redirect, flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from menu import menu
import os
from werkzeug.utils import secure_filename  # к обработке фото


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    defect = db.Column(db.Text, db.ForeignKey(
        'defect.defect_name'))  # ,, nullable=False)
    operation = db.Column(db.Text, db.ForeignKey(
        'operation.operation_name'), nullable=False)
    article = db.Column(db.Text)  # , nullable=False)
    name = db.Column(db.Text)  # ,, nullable=False)
    sort = db.Column(db.Integer)  # ,, nullable=False)
    # picture =
    note = db.Column(db.String(300))  # ,, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Catalog %r, %r, %r, %r, %r, %r, %r>" % (self.defect, self.operation,
                                                      self.article, self.name, self.sort,
                                                      self.note,  self.date)


class Defect(db.Model):
    defect_name = db.Column(db.String(50), nullable=False, primary_key=True)

    def __repr__(self):
        return '<defect_name %r>' % self.defect_name


class Operation(db.Model):
    operation_name = db.Column(db.String(50), nullable=False, primary_key=True)

    def __repr__(self):
        return '<operation_name %r>' % self.operation_name

class Product (db.Model):
    id = db.Column('id', db.Integer, primary_key=True, nullable=True, autoincrement=True)
    article_number = db.Column(db.String(30))
    article_name = db.Column(db.String(30))
    product_name = db.Column(db.String(50))
    def __repr__(self):
        return "<Product %r, %r, %r>" % (self.article_number, self.article_name, self.product_name)

#    def __repr__(self):
#        return "<User(%r, %r)>" % (
#                self.name, self.fullname

# def __init__(self, site_code, site_type, temperature, name):
#        self.name = name
#        self.site_code = site_code
#        self.site_type = site_type
#        self.temperature = temperature


app.config["SECRET_KEY"] = "OB3Ux3QBsUxCdK0ROCQd_w"

##########################################################################################################

@app.route('/')
@app.route('/home')
def index():
    # print(session["USERNAME"])
    # return  """ <h2 style='color: red;'>Hi, Djonny!</h2> """

    return render_template("base1.html", menu=menu)
##########################################################################################################
user_data = {
        "username": "otk",
        "email": "julian@gmail.com",
        "password": "115",
        "bio": "Some guy from the internet"
    
}

@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
        if request.method == 'POST':
                req = request.form
                print (req)
                username = req.get('username')
                password = req.get('password')

                if not username in user_data["username"]:
                        print ("Username not found")
                        print (user_data["username"])
                        return redirect(request.url)
                else:
                        user = user_data["username"]

                if not password == user_data['password']:
                        print ('Incorrect password')
                        return redirect(request.url)
                else:
                        session['USERNAME'] = user_data['username'] 
                        session['PASSWORD'] = user_data['password']      
                        print('Session username set')
                        print(session)
                        # return redirect(request.url)
                        return redirect(url_for("user_profile"))

        return render_template('/sign_in.html')    


##########################################################################################################
@app.route("/user_profile")
def user_profile():

        if not session.get("USERNAME") is None:
                # 
                username = session.get("USERNAME")
                user = user_data["username"]
                return render_template("/user_profile.html",user_data=user_data, user=user)
        else:
                print("No username found is session")
                return redirect(url_for("sign_in"))
        # return render_template("public/user_profile.html", user=user)

##########################################################################################################
app.config["IMAGE_UPLOADS"] = "/home/lem/PROJECTS/catalog/static/img/uploads"
# app.config["IMAGE_UPLOADS"] = "/home/lem/PROJECTS/test/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 4 * 1024 * 1024


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


def upload(n):

    if request.files:
        if "filesize" in request.cookies:
            if not allowed_image_filesize(request.cookies["filesize"]):
                print("Filesize exceeded maximum limit")
                return redirect(request.url)
#####################################################################
        image = n
        # print(image.filename)
        # d = Catalog.query.order_by(Catalog.id.desc()).first()
        # ext = image.filename.rsplit(".", 1)
        # print('file'+str(d.id+1)+'.'+ext[1])
        # fl = ('file_'+str(d.id+1)+'.'+ext[1]).lower()
        # new_name=os.rename(image.filename, fl)
######################################################################
        if image.filename == "":
            print("No filename")
            return redirect(request.url)
        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            d = Catalog.query.order_by(Catalog.id.desc()).first()########
            ext = filename.rsplit(".", 1)###########
            fl = ('file_'+str(d.id+1)+'.'+ext[1]).lower()##############
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], fl))
            print("Image saved")
            return "static/img/uploads"+fl
        else:
            print("That file extension is not allowed")
            return redirect(request.url)

    # print (d.id)

   



##########################################################################################################
@app.route('/add', methods=['POST', 'GET'])
def add():
    e = request.form
    defect = Defect.query.all()
    operation = Operation.query.all()
    # catalog = Catalog.query.all()
    product = Product.query.all()
    print (product)
    for i in e:
        print(i)
    if request.method == "POST":
        # обработчик фото
        if request.form["indetify"] == "form1":
            d = Catalog.query.order_by(Catalog.id.desc()).first()    
            defect_name = (request.form['defect_name']).upper()
            operation_name = (request.form['operation_name']).upper()
            defect_type = (request.form['defect_type'])
            # article_number = (request.form['article_number'])
            product_name = (request.form['product_name']).upper()
            #note = request.files['image']  #????????????????request.form
            ff = request.form
            fl = request.files
            fg = request.cookies
            print(defect_name, operation_name, defect_type,
                  product_name,  d.id)
            print ('new=   ',ff)
            print ('now=   ',fl)
            print ('nrw=   ',fg)
            
            q = Catalog(defect=defect_name,
                        operation=operation_name,
                        sort=defect_type,
                        # article=article_number,
                        name=product_name,
                        #note=note)
                        )
            print ('q=   ',q)

            try:
                db.session.add(q)
                d = Catalog.query.order_by(Catalog.id.desc()).first()
                print (d.id)
                db.session.commit()
                return redirect('/add#1')
            except:
                return "При добавлении произошла ошибка"

        if request.form["indetify"] == "form2":
            defect_name = (request.form['defect_name']).upper()
            defect = Defect(defect_name=defect_name)

            try:
                db.session.add(defect)
                db.session.commit()
                print("form2- передача в базу осуществлена")
                return redirect('/add#2')
            except:
                return "При добавлении произошла ошибка"

        if request.form["indetify"] == "form3":
            operation_name = (request.form['operation_name']).upper()
            operation = Operation(operation_name=operation_name)

            try:
                db.session.add(operation)
                db.session.commit()
                return redirect('/add#3')
            except:
                return "При добавлении произошла ошибка"

    

        if request.form["indetify"] == "form4":
            article_number = (request.form['article_number']).upper()
            article_name = (request.form['article_name']).upper()
            product_name =article_name+', '+article_number
            print (product_name)
            product = Product(article_number=article_number, article_name=article_name, product_name=product_name)
            
            try:
                db.session.add(product)
                db.session.commit()
                flash ('Информация по изделию добавлена в базу данных', 'warning')
                return redirect('/add#4')
            except:
                return "При добавлении произошла ошибка"

    else:
        return render_template("add.html", operation=operation, defect=defect, product=product)

####################################################################
@app.route('/add_catalog', methods=['POST', 'GET'])
def add_catalog():
    defect = Defect.query.all()
    operation = Operation.query.all()
    product = Product.query.all()

    if request.method == "POST":
        # обработчик фото
        d = Catalog.query.order_by(Catalog.id.desc()).first()    
        defect_name = (request.form['defect_name']).upper()
        operation_name = (request.form['operation_name']).upper()
        defect_type = (request.form['defect_type'])
        # article_number = (request.form['article_number'])
        product_name = (request.form['product_name']).upper()
        #note = request.files['image']  #????????????????request.form
        ff = request.form
        fl = request.files
        fg = request.cookies
        print(defect_name, operation_name, defect_type,
                  product_name,  d.id)
        print ('new=   ',ff)
        print ('now=   ',fl)
        print ('nrw=   ',fg)
            
        q = Catalog(defect=defect_name,
                    operation=operation_name,
                    sort=defect_type,
                    # article=article_number,
                    name=product_name,
                    #note=note)
                        )
        print ('q=   ',q)

        try:
            db.session.add(q)
            d = Catalog.query.order_by(Catalog.id.desc()).first()
            print (d.id)
            db.session.commit()
            return redirect('/add_catalog')
        except:
            return "При добавлении произошла ошибка"


    else:
        return render_template("add_catalog.html", operation=operation, defect=defect, product=product)

####################################################################    
@app.route('/add_defect', methods=['POST', 'GET'])
def add_defect():
    defect = Defect.query.all()
    if request.method == "POST":
        defect_name = (request.form['defect_name']).upper()
        defect = Defect(defect_name=defect_name)

        try:
            db.session.add(defect)
            db.session.commit()
            flash("Наименование дефекта добавлено в базу данных", 'warning')
            return redirect('/add_defect')
        except:
            return "При добавлении произошла ошибка"


    else:
        return render_template("add_defect.html", defect=defect)   

####################################################################
@app.route('/add_operation', methods=['POST', 'GET'])
def add_operation():
    operation = Operation.query.all()

    if request.method == "POST":
        operation_name = (request.form['operation_name']).upper()
        operation = Operation(operation_name=operation_name)

        try:
            db.session.add(operation)
            db.session.commit()
            return redirect('/add_operation')
        except:
            return "При добавлении произошла ошибка"

 
    else:
        return render_template("add_operation.html", operation=operation)

####################################################################    
@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    product = Product.query.all()

    if request.method == "POST":
        article_number = (request.form['article_number']).upper()
        article_name = (request.form['article_name']).upper()
        product_name =article_name+', '+article_number
        product = Product(article_number=article_number, article_name=article_name, product_name=product_name)
            
        try:
            
            db.session.add(product)
            db.session.commit()
            flash ('Информация по изделию добавлена в базу данных', 'warning')
            return redirect('/add_product')
        except:
            return "При добавлении произошла ошибка"

    else:
        return render_template("add_product.html", product=product)




####################################################################



@app.route('/show', methods=['POST', 'GET'])
def show():
    req = request.form.get("flexRadioDefault")
    defects = Defect.query.all()
    # d = Catalog.query.order_by(Catalog.operation).all()
    c = Catalog.query.all()
    f = Catalog.query.order_by(Catalog.name).all()
    s = Catalog.query.filter_by(defect='ПЕРЕКОС').all()
    # print(defects)
    # print(type(d))
    # print(c)
    # print('+'*70)
    # print(f)
    # print(req)
    # for i in req:
    # print (i)
    if req == "a":
        d = Catalog.query.order_by(Catalog.defect).all()
    elif req == "b":
        d = Catalog.query.order_by(Catalog.operation).all()
    else:
        d = Catalog.query.order_by(Catalog.id).all()
    return render_template("show.html", defects=defects, d=d, s=s)
@app.route('/show_defect')
def show_defect():
    sd = request.form.get('1234')
    se = request.form.get('12')
    defects = Defect.query.order_by(Defect.defect_name).all()
    d = Catalog.query.order_by(Catalog.defect).all()
    print(sd)
    print(se)
    return render_template("show_defect.html", defects=defects, d=d)


@app.route('/show_defect/<int:id>')
def show_defect_detail(id):
    defect_detail = Catalog.query.get(id)

    return render_template("defect_detail.html", defect_detail=defect_detail)

@app.route('/show_defect/<int:id>/del')
def defect_delete(id):
    defect = Catalog.query.get_or_404(id)
    try:
        db.session.delete(defect)
        
        db.session.commit()
        return redirect('/show_defect')
    except:
        return "При удалении произошла ошибка"



@app.route('/show_operation')
def show_operation():
    operations = Operation.query.order_by(Operation.operation_name).all()

    return render_template("show_operation.html", operations=operations)


@app.route('/1')
def one():
    pr = ["perfect", "beautiful", "nice"]
    defect = Defect.query.all()
    return render_template("1.html", pr=pr, defect=defect)


@app.route('/defect')
def defect():

    return render_template("defect.html")



app.config["IMAGE_UPLOADS"] = "/home/lem/PROJECTS/catalog/static/img/uploads"
# app.config["IMAGE_UPLOADS"] = "/home/lem/PROJECTS/test/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 4 * 1024 * 1024


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        print (request.files)

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)
####################################################################
            image = request.files["image"]
            print(image.filename)
            d = Catalog.query.order_by(Catalog.id.desc()).first()
            ext = image.filename.rsplit(".", 1)
            print('file'+str(d.id+1)+'.'+ext[1])
            fl=('file_'+str(d.id+1)+'.'+ext[1]).lower()
#####################################################################            
            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], fl))

                print("Image saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)




    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)


