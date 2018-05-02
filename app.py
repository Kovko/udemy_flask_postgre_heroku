# importing Flask class from flask module
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# creating an instance of a # class
# name parameter is by default __main__
app = Flask(__name__)

# you need to define SQLALCHEMY db URI
app.config.update(
    SECRET_KEY="7a4ddc0a-5f21-45de-9947-a5a97df3df03**88975af9-6f44-41ea-bf14-01e581b60a73",
    SQLALCHEMY_DATABASE_URI="postgres://postgres:remotepg@localhost:5432/catalog_db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Creating an instance of SQLAlchemy class
db = SQLAlchemy(app)


# creating tables (derived from db.Model class)
class Publication(db.Model):
    # correct table in __tablename__ variable
    __tablename__ = "publication"

    # define columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # constructor
    def __init__(self, id, name):
        self.id = id
        self.name = name

    # always good to override for string output
    def __repr__(self) -> str:
        return "Publication -> id: {}, name: {}".format(self.id, self.name)


# table for relation
class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, index=True)
    author = db.Column(db.String(50), nullable=False)
    avg_rating = db.Column(db.Float)
    num_page = db.Column(db.Integer)
    pub_date = db.Column(db.Date)

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey("publication.id"))

    def __init__(self, title, author, avg_rating, num_page, pub_date, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.num_page = num_page
        self.pub_date = pub_date
        self.pub_id = pub_id

    def __repr__(self):
        return "{} by {}.".format(self.title, self.author)


# address for main page / like www.google.com/
# (last / is optional)
# you can add more then one route to the function
@app.route("/index")
@app.route("/")
def hello_world():
    # function returning a string
    # response from server to the client
    return 'Hello World!'


# you can get request parameters from request object
@app.route("/get/")
def greetings(default_greet="hello"):
    greeting = request.args.get("greeting", default_greet)
    return "<h1>Greeting for now is: {}</h1>".format(greeting)


# you can make an url parametrized - for example for api calls
@app.route("/user/")
@app.route("/user/<name>")
def user_name(name="No user!"):
    return "<h1>Hello {}</h1>".format(name)


# defining of two parameter types
@app.route("/multiply/<float:num1>/<float:num2>")
def multiply(num1, num2):
    return "<h1>{} * {} = {}</h1>".format(num1, num2, num1 * num2)


# render_template function is used to render a template from *.html file
@app.route("/template/")
def template():
    return render_template("hello.html")


# url_for example (adding static content to the page)
@app.route("/url_for/")
def url_for_example():
    return render_template("url_for.html")


# you can attach the parameters to the render_template
@app.route("/jinja2/")
def jinja2():
    item_list = ["item1", "item2", "item3", "item4", "item5"]
    item_dict = {
        "item1": 1,
        "item2": 1,
        "item3": 2,
        "item4": 3,
        "item5": 5,
        "item6": 8
    }
    return render_template("jinja2.html", name="Miro", items=item_list, dicts=item_dict)


@app.route("/filters/")
def filters():
    capitalize = "this i a text"
    rounding = 1.559
    return render_template("filters.html", capitalize=capitalize, rounding=rounding)


@app.route("/macros/")
def macros_example():
    list1 = ["i1", "i2", "i3", "i4"]
    list2 = range(10)
    return render_template("macros_example.html", l1=list1, l2=list2)


def insert_data():
    # inserting data into database (single row)
    pub = Publication(1, "Publication 1")
    db.session.add(pub)
    db.session.commit()

    # inserting data into database (more rows)
    pub2 = Publication(2, "Publication 2")
    pub3 = Publication(3, "Publication 3")
    db.session.add_all([pub2, pub3])
    db.session.commit()

    # inserting some titles
    book1 = Book("Witcher", "Sapkowski", 4.8, 253, date(1999, 7, 8), 1)
    book2 = Book("Witcher 2", "Sapkowski", 4.7, 289, date(2001, 5, 12), 1)
    db.session.add_all([book1, book2])
    db.session.commit()

if __name__ == 'app':
    db.create_all()

    # insert_data()

    # selecting data
    books = Book.query.all()
    for b in books:
        print(b.author, b.title, b.num_page)

    # select only first record
    first_book = Book.query.first()
    print(first_book)

    # select by pk
    pk_book = Book.query.get(2)
    print(pk_book)

    # select with condition
    book_filtered = Book.query.filter_by(author="Sapkowski").all()
    print("Filtered", book_filtered)

    # ordering
    book_ordered = Book.query.order_by(Book.avg_rating).all()
    print("Ordered", book_ordered)

    # updating a record
    book_update = Book.query.get(1)
    if book_update:
        book_update.author = 'Andrej Sapkowski'
        db.session.commit()

    # deleting records
    book_delete = Book.query.get(2)
    if book_delete:
        db.session.delete(book_delete)
        db.session.commit()

    # another delete with filter
    Book.query.filter_by(author="Andrej Sapkowski").delete()
    db.session.commit()


#print("App name:", __name__)
#if __name__ == '__main__':
    # create all tables
    #db.create_all()
    # try to Debug if not release build
#    app.run(debug=True)
