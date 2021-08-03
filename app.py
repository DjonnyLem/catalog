from flask import Flask, render_template, url_for, request, redirect, flash, session
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
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    id_defect = db.Column(db.Integer, db.ForeignKey(
        'defect.id'))  # ,, nullable=False)
    id_operation = db.Column(db.Integer, db.ForeignKey(
        'operation.id'), nullable=False)
    id_product = db.Column(db.Text, db.ForeignKey(
        'product.id'), nullable=False)
    defect_type = db.Column(db.Integer)  # ,, nullable=False)
    picture = db.Column(db.Text)  # ,, nullable=False)
    note = db.Column(db.String(300))  # ,, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Catalog %r, %r, %r, %r, %r, %r, %r" % (self.id_defect, self.id_operation, self.id_product, self.defect_type,
                                                             self.picture, self.note,  self.date)


class Defect(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    defect_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<defect_name %r, %r>' % (self.id, self.defect_name)


class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    operation_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<operation_name %r, %r>' % (self.id, self.operation_name)


class Product (db.Model):
    id = db.Column('id', db.Integer, primary_key=True,
                   nullable=True, autoincrement=True)
    article_number = db.Column(db.String(30))
    article_name = db.Column(db.String(30))
    general_name = db.Column(db.String(50))

    def __repr__(self):
        return "<Product %r, %r, %r>" % (self.article_number, self.article_name, self.general_name)

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

    return render_template("home.html", menu=menu)


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
        username = req.get('username')
        password = req.get('password')

        if not username in user_data["username"]:
            flash("Не верный логин или пароль", 'danger')
            return redirect(request.url)
        else:
            user = user_data["username"]

        if not password == user_data['password']:
            flash("Не верный логин или пароль", 'danger')
            return redirect(request.url)
        else:
            #session['USERNAME'] = user_data['username']
            #session['PASSWORD'] = user_data['password']
            session['AUTHORIZATION'] = 'OK'
            print('Session username set')
            print(session)
            # return redirect(request.url)
            return redirect(url_for("index"))

    return render_template('/sign_in.html')


##################################################################
@app.route("/user_profile")
def user_profile():

    if not session.get("USERNAME") is None:
        #
        username = session.get("USERNAME")
        user = user_data["username"]
        return render_template("/user_profile.html", user_data=user_data, user=user)
    else:
        print("No username found is session")
        return redirect(url_for("sign_in"))
    # return render_template("public/user_profile.html", user=user)

####################################################################



####################################################################
app.config["IMAGE_UPLOADS"] = "static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 2 * 1024 * 1024
path = os.getcwd()


# проверяем имеет ли файл расширение и допустимо ли такое расширение
def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def addFile():
    pass


def limit_filesize(filesize):  # Проверяем не превышает ли файл допустимый объем

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


'''
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

'''


#########################################################################
@app.route('/add_catalog', methods=['POST', 'GET'])
def add_catalog():
    defect = Defect.query.all()
    operation = Operation.query.all()
    product = Product.query.all()

    if request.method == "POST":

        d = Catalog.query.order_by(Catalog.id.desc()).first()
        id_defect = (request.form['defect_name'])
        id_operation = (request.form['operation_name'])
        defect_type = (request.form['defect_type'])
        id_product = (request.form['product_name']).upper()
        note = (request.form['note']).upper()
        image = request.files['image']
        print(id_defect)
        if request.files:
            if "filesize" in request.cookies:
                if not limit_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    flash("Размер файла превышает лимит", 'warning')
                    return redirect(request.url)

            if image.filename == "":
                print("No filename")
                flash("Файл не выбран", 'warning')
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("Расширение файла не соответствует заданному")
                flash("Расширение файла не соответствует заданному", 'warning')
                filename = secure_filename(image.filename)
                return redirect(request.url)

            print("picture =", image.filename)
            e = image.filename.rsplit('.', 1)
            past_id = Catalog.query.order_by(Catalog.id.desc()).first()

            if past_id is None:
                num_id = 0
            else:
                num_id = past_id.id
            print("past_id =", num_id)
            new_flname = "file_"+str(num_id+1)+"."+(e[1]).lower()
            flname = secure_filename(new_flname)
            print(flname)
            path_flname = os.path.join(app.config["IMAGE_UPLOADS"], flname)
            print(path_flname)

            print(path)
            path_load = os.path.join(path, app.config["IMAGE_UPLOADS"])
            print("path_load=", path_load)

        picture = path_flname

        ff = request.form
        fl = request.files
        fg = request.cookies
        print(id_defect, id_operation, defect_type,
              id_product, note)
        print('new=   ', ff)
        print('now=   ', fl)
        print('nrw=   ', fg)

        q = Catalog(id_defect=id_defect,
                    id_operation=id_operation,
                    defect_type=defect_type,
                    picture=picture,
                    id_product=id_product,
                    note=note)

        print('q=   ', q)

        try:
            db.session.add(q)
            d = Catalog.query.order_by(Catalog.id.desc()).first()
            print(d.id)
            image.save(os.path.join(path_load, flname))
            db.session.commit()
            return redirect('/add_catalog')
        except:
            return "При добавлении произошла ошибка"

    else:
        return render_template("add_catalog.html",
                               operation=operation,
                               defect=defect,
                               product=product)

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
        general_name = article_name+', '+article_number
        product = Product(article_number=article_number,
                          article_name=article_name, general_name=general_name)

        try:

            db.session.add(product)
            db.session.commit()
            flash('Информация по изделию добавлена в базу данных', 'warning')
            return redirect('/add_product')
        except:
            return "При добавлении произошла ошибка"

    else:
        return render_template("add_product.html", product=product)


####################################################################
# table_head = ('#', '#', 'Наименование изделия', 'Дефект', 'Операция', 'Фото', 'Комментарии', 'Расположение')
table_head = ('Наименование изделия', 'Дефект', 'Операция',
              'Комментарии', 'Фото')  # Описываем колонки таблицы
####################################################################


@app.route('/show_catalog')
def show_catalog():
    # defects = Defect.query.all()#order_by(Defect.defect_name).all()
    # catalog = Catalog.query.order_by(Catalog.id_defect).all()
    # cat = Catalog.query.order_by(Catalog.id_defect).distinct(Catalog.id_defect).all()
    #res = db.session.query(Catalog.defect).join(Defect).distinct().all()
    #res =(sum(res,()))
    defects = db.session.query(Defect.id, Defect.defect_name).join(
        Catalog).distinct().order_by(Defect.defect_name).all()
    #catalog= db.session.query(Catalog, Defect.defect_name).join(Defect).order_by(Defect.defect_name).all()
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name, Product.general_name).join(
        Defect, Operation, Product).order_by(Defect.defect_name).all()
# Показываем наименование дефекта из таблице Дефект
    #res = res.sort()
    

    return render_template("show_catalog.html", defects=defects, catalog=catalog, table_head=table_head)


####################################################################
@app.route('/show_catalog/<int:id>')
def select_defect(id):
    defects = db.session.query(Defect.id, Defect.defect_name).join(
        Catalog).distinct().order_by(Defect.defect_name).all()
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name, Product.general_name).join(
        Defect, Operation, Product).order_by(Defect.defect_name).filter(Defect.id == id)

    #   db.session.query(Yahoo.price).filter_by(ticker=self.ticker).order_by(
   # db.desc(Yahoo.date)).first()[0])

    return render_template("show_catalog.html", defects=defects, catalog=catalog, table_head=table_head)

####################################################################


@app.route('/catalog_list/<int:id>')
def catalog_list(id):
            
    catalog_list = db.session.query(Catalog).get(id)
    defect_list = db.session.query(Defect).filter(
        catalog_list.id_defect == Defect.id)
    operation_list = db.session.query(Operation).filter(
    catalog_list.id_operation == Operation.id)
    product_list = db.session.query(Product).filter(
    catalog_list.id_product == Product.id)
    return render_template("catalog_list.html",
                           operation_list=operation_list,
                           catalog_list=catalog_list,
                           defect_list = defect_list,
                           product_list=product_list)
####################################################################


@app.route('/catalog_list/<int:id>/del')
def catalog_delete(id):
    catalog = Catalog.query.get_or_404(id)
    try:
        d = os.path.join(path, catalog.picture)
        print(d)
        if os.path.isfile(d):
            os.remove(d)
        db.session.delete(catalog)

        db.session.commit()
        return redirect('/show_catalog')
    except:
        return "При удалении произошла ошибка"
# >>> if os.path.isfile ('/home/tech-3/Рабочий стол/1.txt'):
#  os.remove('/home/tech-3/Рабочий стол/1.txt')

#


####################################################################
@app.route('/catalog_list/<int:id>/update', methods=['POST', 'GET'])
def catalog_update(id):
    catalog = Catalog.query.get(id)
    defect = Defect.query.all()
    operation = Operation.query.all()
    product = Product.query.all()
    if request.method == "POST":
        print('POST')
        catalog.id_defect = (request.form['defect_name']).upper()
        catalog.id_operation = (request.form['operation_name']).upper()
        catalog.defect_type = (request.form['defect_type'])
        catalog.id_product = (request.form['product_name']).upper()
        catalog.note = (request.form['note']).upper()
        if not request.files['image']:
            print("None")

        else:
            print('OK')  # ????????????????request.form
            image = request.files['image']
            if "filesize" in request.cookies:
                if not limit_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    flash("Размер файла превышает лимит", 'warning')
                    return redirect(request.url)

            if image.filename == "":
                print("No filename")
                flash("Файл не выбран", 'warning')
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("Расширение файла не соответствует заданному")
                flash("Расширение файла не соответствует заданному", 'warning')
                filename = secure_filename(image.filename)
                return redirect(request.url)

            splitFile = image.filename.rsplit('.', 1)
            print(splitFile)

            newFileName = "file_"+str(id)+"."+(splitFile[1]).lower()
            fileName = secure_filename(newFileName)
            print(fileName)
            pathFileName = os.path.join(app.config["IMAGE_UPLOADS"], fileName)
            print(pathFileName)

            print(path)
            pathLoad = os.path.join(path, app.config["IMAGE_UPLOADS"])
            print("pathLoad=", pathLoad)

            picture = pathFileName

            catalog = Catalog.query.get_or_404(id)
            try:
                pathOldFile = os.path.join(path, catalog.picture)
                print('pathOldFile =', pathOldFile)
                if os.path.isfile(pathOldFile):
                    os.remove(pathOldFile)
                    print("Удалено")
            except:
                return "При удалении произошла ошибка"
            image.save(os.path.join(pathLoad, fileName))
            catalog.picture = picture
        try:
            db.session.commit()
            print('Изменено')
            return redirect('/show_catalog')
        except:
            return "При редактировании произошла ошибка"
    else:
        return render_template("catalog_update.html", catalog=catalog,
                               defect=defect, operation=operation,
                               product=product)
####################################################################


@app.route('/show_operation')
def show_operation():

    operations = db.session.query(Operation.id, Operation.operation_name).join(
        Catalog).distinct().order_by(Operation.operation_name).all()
    
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name, Product.general_name).join(
        Defect, Operation, Product).order_by(Operation.operation_name).all()


    return render_template("show_operation.html",
                           operations=operations,
                           catalog=catalog,
                           table_head=table_head)


####################################################################

@app.route('/show_operation/<int:id>')
def select_operation(id):
    
    operations = db.session.query(Operation.id, Operation.operation_name).join(
        Catalog).distinct().order_by(Operation.operation_name).all()
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name,
    Product.general_name).join(Defect, Operation, Product).order_by(Operation.operation_name).filter(Operation.id == id)

  

    return render_template("show_operation.html", operations=operations, catalog=catalog, table_head=table_head)

####################################################################

@app.route('/show_product')
def show_product():

    products = db.session.query(Product.id, Product.general_name).join(
        Catalog).distinct().order_by(Product.general_name).all()
    
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name, Product.general_name).join(
        Defect, Operation, Product).order_by(Product.general_name).all()


    return render_template("show_product.html",
                           products=products,
                           catalog=catalog,
                           table_head=table_head)


####################################################################

@app.route('/show_product/<int:id>')
def select_product(id):
    
    products = db.session.query(Product.id, Product.general_name).join(
        Catalog).distinct().order_by(Product.general_name).all()
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name,
    Product.general_name).join(Defect, Operation, Product).order_by(Product.general_name).filter(Product.id == id)

  

    return render_template("show_product.html",
                           products=products,
                           catalog=catalog,
                           table_head=table_head)

####################################################################

@app.route('/defect/<int:id>/update', methods=['POST', 'GET'],)
def defect_update(id):
    defect_list = Defect.query.get(id)
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name, Product.general_name).join(
        Defect, Operation, Product).order_by(Defect.defect_name).filter(Defect.id == id)

    if request.method == "POST":
        if request.form['defect_name'] != "":
 #           catalog.id_defect = (request.form['defect_name']).upper()
            defect_list.defect_name = (request.form['defect_name']).upper()

            try:
                db.session.commit()
                print('Изменено')
                return redirect('/add_defect')
            except:
                return "При редактировании произошла ошибка"
        else:
            return redirect('/add_defect')
    else:
        return render_template("defect_update.html",
                               defect_list=defect_list,
                               catalog=catalog,
                               table_head=table_head)


####################################################################
@app.route('/defect/<int:id>/del', methods=['POST', 'GET'],)
def defect_delete(id):
    defect_list = Defect.query.get_or_404(id)
    # catalog = db.session.query(Catalog, Defect.defect_name).join(
        # Defect).order_by(Defect.defect_name).filter(Defect.id == id)

    catalog = db.session.query(Catalog).filter_by(id_defect=id)
    if catalog.first() is not None:
        print ('Catalog contains ID')
        try:
            for i in catalog:
                print('i =', i.picture)
                d = os.path.join(path, i.picture)
                if os.path.isfile(d):
                    os.remove(d)
                db.session.delete(i)
                db.session.commit()
            db.session.delete(defect_list)
            db.session.commit()
            return redirect('/add_defect')
        except:
            return "При удалении произошла ошибка"
        
    else:
        print ('Catalog not contains ID')
        try:
            db.session.delete(defect_list)
            db.session.commit()
            return redirect('/add_defect')
        except:
            return "При удалении произошла ошибка"
      
            

####################################################################


@app.route('/operation/<int:id>/update', methods=['POST', 'GET'],)
def operation_update(id):
    operation_list = Operation.query.get(id)
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name, Product.general_name).join(
        Defect, Operation, Product).order_by(Operation.operation_name).filter(Operation.id == id)

    if request.method == "POST":
        if request.form['operation_name'] != "":
#            catalog.id_operation = (request.form['operation_name']).upper()
            operation_list.operation_name = (request.form['operation_name']).upper()

            try:
                db.session.commit()
                print('Изменено')
                return redirect('/add_operation')
            except:
                return "При редактировании произошла ошибка"
        else:
            return redirect('/add_operation')
    else:
        return render_template("operation_update.html",
                               operation_list=operation_list,
                               catalog=catalog,
                               table_head=table_head)


####################################################################
@app.route('/operation/<int:id>/del', methods=['POST', 'GET'],)
def operation_delete(id):
    operation_list = Operation.query.get_or_404(id)
 ##   catalog = db.session.query(Catalog, Operation.operation_name).join(
 ##       Operation).order_by(Operation.operation_name).filter(Operation.id == id)

    catalog = db.session.query(Catalog).filter_by(id_operation=id)


    if catalog.first() is not None:
        print ('Catalog contains ID')
        try:
            for i in catalog:
                print('i =', i.picture)
                d = os.path.join(path, i.picture)
                if os.path.isfile(d):
                    os.remove(d)
                db.session.delete(i)
                db.session.commit()
            db.session.delete(operation_list)
            db.session.commit()
            return redirect('/add_operation')
        except:
            return "При удалении произошла ошибка"
        
    else:
        print('Catalog not contains ID')
        try:
            db.session.delete(operation_list)
            db.session.commit()
            return redirect('/add_operation')
        except:
            return "При удалении произошла ошибка"


####################################################################

@app.route('/product/<int:id>/update', methods=['POST', 'GET'],)
def product_update(id):
    product_list = Product.query.get(id)
    catalog = db.session.query(Catalog, Defect.defect_name, Operation.operation_name, Product.general_name).join(
        Defect, Operation, Product).order_by(Product.general_name).filter(Product.id == id)

    if request.method == "POST":
        if request.form['article_number'] == "" and request.form['article_name'] != "":
            product_list.article_name = (request.form['article_name']).upper()            
            product_list.general_name = f"{(request.form['article_name']).upper()}, {product_list.article_number}"
        elif request.form['article_number'] != "" and request.form['article_name'] == "":
            product_list.article_number = (request.form['article_number']).upper()
            product_list.general_name = f"{product_list.article_name}, {(request.form['article_number']).upper()}"
        elif request.form['article_number'] != "" and request.form['article_name'] != "":
            #catalog.id_operation = (request.form['operation_name']).upper()
            product_list.article_number = (request.form['article_number']).upper()
            product_list.article_name = (request.form['article_name']).upper()            
            product_list.general_name = f"{(request.form['article_name']).upper()}, {(request.form['article_number']).upper()}"
        else:
            return redirect('/add_product')

        try:
            db.session.commit()
            print('Изменено')
            return redirect('/add_product')
        except:
            return "При редактировании произошла ошибка"
        
    else:
        return render_template("product_update.html",
                               product_list=product_list,
                               catalog=catalog,
                               table_head=table_head)




####################################################################
@app.route('/product/<int:id>/del', methods=['POST', 'GET'],)
def product_delete(id):
    product_list = Product.query.get_or_404(id)
    catalog = db.session.query(Catalog).filter_by(id_product=id)
    if catalog.first() is not None:
        print ('Catalog contains ID')
        try:
            for i in catalog:
                print('i =', i.picture)
                d = os.path.join(path, i.picture)
                if os.path.isfile(d):
                    os.remove(d)

                db.session.delete(i)
                db.session.commit()
            db.session.delete(product_list)
            db.session.commit()
            return redirect('/add_product')
        except:
            return "При удалении произошла ошибка"
        
    else:
        print ('Catalog not contains ID')
        try:
            db.session.delete(product_list)
            db.session.commit()
            return redirect('/add_product')
        except:
            return "При удалении произошла ошибка"
        
    
####################################################################
if __name__ == "__main__":
    app.run(debug=True)


