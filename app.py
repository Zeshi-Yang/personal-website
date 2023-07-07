from flask import Flask,render_template,Blueprint,g,request, render_template_string, url_for
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

@research_bp.route('/')
def research():
    db = get_db()
    cursor = db.execute('SELECT * FROM research_projects')
    intros = cursor.fetchall()
    return render_template('research.html',intros=intros)

@app.context_processor
def inject_intros():
    db = get_db()
    research_cursor = db.execute('SELECT * FROM research_projects')
    research_intros = research_cursor.fetchall()
    programming_cursor = db.execute('SELECT * FROM programming_projects')
    programming_intros = programming_cursor.fetchall()
    return dict(research_intros=research_intros, programming_intros=programming_intros)

@app.route('/research/<int:intro_id>')
def show_intro_1(intro_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM research_projects')
    intros = cursor.fetchall()
    # Retrieve the introduction from the database based on the intro_id
    # Render and return the template that displays the introduction
    return render_template('/research projects/research_projects.html',intro=intros[intro_id-1])

@app.route('/programming/<int:intro_id>')
def show_intro_2(intro_id):

    db = get_db()

    cursor = db.execute('SELECT * FROM programming_projects')

    intros = cursor.fetchall()
    # Retrieve the introduction from the database based on the intro_id
    # Render and return the template that displays the introduction

    # Generate the image source for the specific intro_id
    image_src = url_for('static', filename=f'images/{intro_id}.png')

    return render_template('/programming projects/programming_projects.html',intro=intros[intro_id-1],image_src=image_src)


@app.route('/')
def home():
    return render_template('index.html',person=person)

@app.route('/trading')
def trading():

    return render_template('trading.html')

# Create a blueprint for the research sub-website
programming_bp=Blueprint('programming',__name__,url_prefix='/programming')

@programming_bp.route('/')
def programming():
    db = get_db()
    cursor = db.execute('SELECT * FROM programming_projects')
    intros = cursor.fetchall()
    return render_template('programming.html',intros=intros)


@app.route('/contact')
def contact():

    return render_template('contact.html',person=person)

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        email = request.form['email']
        question = request.form['question']

        # Store the form data as required
        # You can write the code to store the data in a database, file, or any other storage method
        db = get_db()
        cursor=db.execute("INSERT INTO contact (email, question) VALUES (?, ?)", (email,question))

        # Commit the changes to the database
        db.commit()

        return render_template_string("""
            <script>
                alert("Form submitted successfully");
                window.history.back();
            </script>
        """)

@app.route('/test')
def test():

    return render_template('test.html')

# Register the blueprint
app.register_blueprint(research_bp)
app.register_blueprint(programming_bp)


if __name__=='__main__':
    app.debug=True
    app.run()    