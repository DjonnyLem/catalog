from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    defect = db.Column(db.Text, db.ForeignKey('defect.defect_name'), nullable=False)
    operation = db.Column(db.Text, db.ForeignKey('operation.operation_name'), nullable=False)
    aricle = db.Column(db.Text, nullable=False)
    name =  db.Column(db.Text, nullable=False)
    sort = db.Column(db.Integer, nullable=True)
    #picture =
    note = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return (f"<catalog>" % self.defect, self.operation,
                self.aricle, self.name, self.sort,
                self.note1, self.note2, self.date)

class Defect(db.Model):
    defect_name = db.Column(db.String(50), nullable=False, primary_key=True)
    def __repr__(self):
        return '<defect %r>' % self.defect_name

class Operation(db.Model):
    operation_name = db.Column(db.String(50), nullable=False, primary_key=True)
    def __repr__(self):
        return '<defect %r>' % self.operation_name

#    def __repr__(self):
#        return "<User(%r, %r)>" % (
#                self.name, self.fullname

#def __init__(self, site_code, site_type, temperature, name):
#        self.name = name
#        self.site_code = site_code
#        self.site_type = site_type
#        self.temperature = temperature


@app.route('/add', methods=['POST', 'GET'])
def add():
    print (request.form)
    defect = Defect.query.all()
    operation = Operation.query.all()
    if request.method == "POST":
        for key, item in request.form.items():
            print (key)
            print (item)
            
            if key =='defect_name':
                
                print("1", item)
                defect_name = (request.form['defect_name']).upper()
                defect = Defect(defect_name=defect_name)
        
                try:
                    db.session.add(defect)
                    db.session.commit()
                    return redirect('/add')
                except:
                    return "При добавлении статьи произошла ошибка"
                  


            
            elif key =='operation_name':
                print("2", item)
                
                print("1", item)
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
'''    
    if request.method == "POST":
        defect_name = (request.form['defect_name']).upper()
        print (defect_name)
        defect = Defect(defect_name=defect_name)
        
        try:
            db.session.add(defect)
            db.session.commit()
            return redirect('/add')
        except:
            #flash('Ошибка отправки')
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("add.html",defect=defect)
'''

        
@app.route('/add')    
def show():
    operation = Operation.query.all()
    return render_template("add.html",operation=operation)
      

@app.route('/1')

def one():
    pr = ["perfect", "beautiful", "nice"]
    defect = Defect.query.all()
    return render_template("1.html", pr=pr,defect=defect)

def one1():
    num = ["one", "two", "three"]
    op = Operation.query.all()
    return render_template("1.html", num=num,op=op)




#    def __repr__(self):
#        return '<Article %r>' % self.id
    
#class Article1(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#   defect = db.Column(db.Text, nullable=False)
#    operation = db.Column(db.Text, nullable=False)
#    aricle = db.Column(db.Text, nullable=False)
#    name =  db.Column(db.Text, nullable=False)
    #sort = db.Column(db.Integer, nullable=True)
    #picture =
#    note1 = db.Column(db.String(300), nullable=False)
#    note2 = db.Column(db.String(300), nullable=False)
#    date = db.Column(db.DateTime, default=datetime.utcnow)
    
#    def __repr__(self):
#        return '<Article1 %r>' % self.id

#@app.route('/')
#@app.route('/home')
#def index():
#    return render_template("index.html")


#@app.route('/about')
#def about():
#    return render_template("about.html")


#@app.route('/posts')
#def posts():
#    articles = Article.query.order_by(Article.date.desc()).all()
#    return render_template("posts.html", articles=articles)


#@app.route('/posts/<int:id>')
#def post_detail(id):
#    article = Article.query.get(id)
#    return render_template("post-detail.html", article=article)


#@app.route('/posts/<int:id>/del')
#def post_delete(id):
#    article = Article.query.get_or_404(id)

#    try:
#        db.session.delete(article)
#        db.session.commit()
#        return redirect('/posts')
#    except:
#        return "При удалении статьи произошла ошибка"


#@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
#def post_update(id):
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



#@app.route('/create-article', methods=['POST', 'GET'])

#def create_article():
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
