from flask import Flask,render_template,Blueprint,g,request
import sqlite3

DATABASE='test.db'

app=Flask(__name__)
app.config.from_object(__name__)

def get_db():
    db=getattr(g,'_database', None)
    if db is None:
        db=g._datase=sqlite3.connect(app.config['DATABASE'])
        db.row_factory=sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class Person:

    def __init__(self, name,age=0):
        self.name = name      
        self.age = age      

    def contact(self,email='',phone='',location=''):
        self.email=email
        self.phone=phone
        self.location=location    

    def self_introduction(self,introduction=''):
        self.introduction=introduction

person=Person('Yang Zeshi',28)
person.contact('yangzeshi@u.nus.edu','+(86)18808263521', 'Singapore')
person.introduction="""
    <p>Hi! My name is Yang Zeshi. Welcome to my website!</p>
    <p>I am a Ph.D. candidate in National Unversity of Singpoare. 
    My jajor is Mechnical Engineering. 
    My research interest includes the additive manufacutring process, the powder dynamics for metall additive manufauctring.</p>
    <p>The journy of studing will come to an end in 2024, and I am excited to explore the new challenges.</p>
    <p>I belive it will be a wonderful journy when moving towards the top supply chain.</p>
    """


# Create a blueprint for the research sub-website
research_bp=Blueprint('research',__name__,url_prefix='/research')

@app.context_processor
def inject_intros():
    db = get_db()
    cursor = db.execute('SELECT * FROM research_projects')
    intros = cursor.fetchall()
    return dict(intros=intros)

@research_bp.route('/')
def research():
    db = get_db()
    cursor = db.execute('SELECT * FROM research_projects')
    intros = cursor.fetchall()
    return render_template('research.html',intros=intros)

@app.route('/research/<int:intro_id>')
def show_intro(intro_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM research_projects')
    intros = cursor.fetchall()
    # Retrieve the introduction from the database based on the intro_id
    # Render and return the template that displays the introduction
    return render_template('/research projects/research_projects.html',intro=intros[intro_id-1])


@app.route('/')
def home():
    return render_template('home.html',person=person)

@app.route('/trading')
def trading():

    return render_template('trading.html')

# Create a blueprint for the research sub-website
programming_bp=Blueprint('programming',__name__,url_prefix='/programming')

@programming_bp.route('/')
def programming():

    return render_template('programming.html')


@app.route('/contact')
def contact():

    return render_template('test.html')

@app.route('/test')
def test():

    return render_template('test.html')

# Register the blueprint
app.register_blueprint(research_bp)
app.register_blueprint(programming_bp)

# Create and populate the SQLite database with sample introduction data
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

@app.route('/add_intro', methods=['GET', 'POST'])
def add_intro():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        insert_command = "INSERT INTO introductions (title, content) VALUES (?, ?)"
        cursor.execute(insert_command, (title, content))
        conn.commit()
        conn.close()

        return "New intro added successfully!"

    return render_template('add_intro.html')

if __name__=='__main__':
    app.debug=True
    app.run()    