from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from menu import menu



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
        return "<User %r, %r, %r, %r, %r, %r, %r>" % (self.defect, self.operation,
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

#    def __repr__(self):
#        return "<User(%r, %r)>" % (
#                self.name, self.fullname

# def __init__(self, site_code, site_type, temperature, name):
#        self.name = name
#        self.site_code = site_code
#        self.site_type = site_type
#        self.temperature = temperature


@app.route('/')
@app.route('/home')
def index():
    # return  """ <h2 style='color: red;'>Hi, Djonny!</h2> """

    return render_template("base1.html", menu=menu)


@app.route('/add', methods=['POST', 'GET'])
def add():
    e = request.form
    defect = Defect.query.all()
    operation = Operation.query.all()
    catalog = Catalog.query.all()
    for i in e:
        print(i)
    if request.method == "POST":

        if request.form["indetify"] == "form1":

            defect_name = (request.form['defect_name1']).upper()
            operation_name = (request.form['operation_name1']).upper()
            defect_type = (request.form['defect_type'])
            article_number = (request.form['article_number'])
            article_name = (request.form['article_name']).upper()
            note = (request.form['note']).upper()
            print(defect_name, operation_name, defect_type,
                  article_number, article_name)

            q = Catalog(defect=defect_name,
                        operation=operation_name,
                        sort=defect_type,
                        article=article_number,
                        name=article_name,
                        note=note)

#            defect = Catalog(defect=defect_name)
#            operation = Catalog(operation=operation_name)
#            sort = Catalog(sort=defect_type)
#            article = Catalog(article=article_number)
#            name = Catalog(name=article_name)
#            note = Catalog(note1=note)

            try:
                db.session.add(q)
 #               db.session.add(operation)
 #               db.session.add(sort)
#                db.session.add(article)
 #               db.session.add(name)
                db.session.commit()
                return redirect('/add')
            except:
                return "При добавлении статьи произошла ошибка"

        if request.form["indetify"] == "form2":
            defect_name = (request.form['defect_name']).upper()
            defect = Defect(defect_name=defect_name)

            try:
                db.session.add(defect)
                db.session.commit()
                print("form2- передача в базу осуществлена")
                return redirect('/add')
            except:
                return "При добавлении статьи произошла ошибка"

        if request.form["indetify"] == "form3":
            operation_name = (request.form['operation_name']).upper()
            operation = Operation(operation_name=operation_name)

            try:
                db.session.add(operation)
                db.session.commit()
                return redirect('/add')
            except:
                return "При добавлении статьи произошла ошибка"

    else:
        return render_template("add.html", operation=operation, defect=defect)


@app.route('/show', methods=['POST', 'GET'])
def show():
    req = request.form.get("flexRadioDefault")
    defects = Defect.query.all()
    #d = Catalog.query.order_by(Catalog.operation).all()
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
    #print (i)
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


#    def __repr__(self):
#        return '<Article %r>' % self.id

# class Article1(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#   defect = db.Column(db.Text, nullable=False)
#    operation = db.Column(db.Text, nullable=False)
#    article = db.Column(db.Text, nullable=False)
#    name =  db.Column(db.Text, nullable=False)
    #sort = db.Column(db.Integer, nullable=True)
    # picture =
#    note1 = db.Column(db.String(300), nullable=False)
#    note2 = db.Column(db.String(300), nullable=False)
#    date = db.Column(db.DateTime, default=datetime.utcnow)

#    def __repr__(self):
#        return '<Article1 %r>' % self.id

# @app.route('/')
# @app.route('/home')
# def index():
#    return render_template("index.html")


# @app.route('/about')
# def about():
#    return render_template("about.html")


# @app.route('/posts')
# def posts():
#    articles = Article.query.order_by(Article.date.desc()).all()
#    return render_template("posts.html", articles=articles)


# @app.route('/posts/<int:id>')
# def post_detail(id):
#    article = Article.query.get(id)
#    return render_template("post-detail.html", article=article)


# @app.route('/posts/<int:id>/del')
# def post_delete(id):
#    article = Article.query.get_or_404(id)

#    try:
#        db.session.delete(article)
#        db.session.commit()
#        return redirect('/posts')
#    except:
#        return "При удалении статьи произошла ошибка"


# @app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
# def post_update(id):
#    article = Article.query.get(id)
#    if request.method == "POST":
#        article.title = request.form['title']
#        article.intro = request.form['intro']
#        article.text = request.form['text']

#        try:
#            db.session.commit()
#            return redirect('/posts')
#        except:
#            return "При редактировании статьи произошла ошибка"
#    else:
#        return render_template("post_update.html", article=article)


# @app.route('/create-article', methods=['POST', 'GET'])

# def create_article():
#    if request.method == "POST":
#        title = request.form['title']
#        intro = request.form['intro']
#        text = request.form['text']
#
#        article = Article(title=title, intro=intro, text=text)

#        try:
#            db.session.add(article)
#            db.session.commit()
#            return redirect('/posts')
#        except:
#            return "При добавлении статьи произошла ошибка"
#    else:
#        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)
