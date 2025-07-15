# Python
from flask import Flask, render_template, Blueprint, g, request, render_template_string, url_for, session, current_app
import sqlite3
import os
from socket import gethostname

DATABASE='test.db'

app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'my_secret_key'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

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

person=Person('Yang Zeshi',30)
person.contact('yangzeshi997@gmail.com',' +(65) 86076345', 'Singapore')
person.introduction="""
    <!-- Intro Section (Professional Tone) -->
    <p>
    <strong>Welcome&nbsp;— I’m Dr.&nbsp;YANG&nbsp;Zeshi.</strong>
    </p>

    <p>
    I am an engineer with complementary foundations in mineral extraction and ferrous metallurgy (B.Eng.&nbsp;Mineral Engineering, M.Eng.&nbsp;Ferrous Metallurgy, Ph.D.&nbsp;Mechanical Engineering).  
    This multidisciplinary path has given me a panoramic view of the industrial value chain—from ore beneficiation and metallurgical conversion to advanced manufacturing processes.
    </p>

    <p>
    Over the past years, I have also built quantitative, data-driven tools for public equity investing.  
    During a recent engagement at a Singapore family office, I designed automated investment research pipelines with modular functions such as <a href="/investment_research/1">stock screening</a>, <a href="/investment_research/2">company analysis</a>, DCF modeling, <a href="/investment_research/3">news filtering intelligence</a>, and <a href="/investment_research/4">macro-indicator tracking</a>, turning complex datasets into decisive portfolio insights.
    </p>

    <p>
    <strong>What I’m looking for now</strong>  
    <br>
    I’m keen to collaborate with research-oriented teams that operate at the intersection of engineering, data science, and capital markets.  
    If your organisation values rigorous analysis, creative problem-solving, and hands-on execution, let’s explore how we can work together.
    </p>

    <p>
    <em>Feel free to connect via&nbsp;<a href="mailto:yangzeshi997@gmail.com">email</a>&nbsp;or&nbsp;<a href="https://www.linkedin.com/in/zeshi-yang">LinkedIn</a>. I look forward to building something impactful with you.</em>
    </p>
"""
# Create a blueprint for the research sub-website
research_bp=Blueprint('research',__name__,url_prefix='/academic_research')

@research_bp.route('/')
def research():
    db = get_db()
    cursor = db.execute('SELECT * FROM research_projects')
    intros = cursor.fetchall()
    session['intro_id'] = 0
    return render_template('academic_research.html',intros=intros)

@app.context_processor
def inject_intros():
    db = get_db()
    research_cursor = db.execute('SELECT * FROM research_projects')
    research_intros = research_cursor.fetchall()
    programming_cursor = db.execute('SELECT * FROM programming_projects')
    programming_intros = programming_cursor.fetchall()

    # Get intro_id from the request or any other source
    intro_id = session.get('intro_id')

    return dict(research_intros=research_intros, programming_intros=programming_intros, intro_id=intro_id)

@app.route('/academic_research/<int:intro_id>')
def show_intro_1(intro_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM research_projects')
    intros = cursor.fetchall()

    # Store intro_id in session
    session['intro_id'] = intro_id

    # Generate the image source for the specific intro_id
    image_src = [url_for('static', filename=f'images/research/{intro_id}.png')]

    file_path = image_src[0].lstrip('/')

    if os.path.exists(file_path)==False:
        image_src=['']

    # Retrieve the introduction from the database based on the intro_id
    # Render and return the template that displays the introduction
    return render_template('/research projects/research_projects.html',intro=intros[intro_id-1],image_srcs=image_src)

@app.route('/investment_research/<int:intro_id>')
def show_intro_2(intro_id):

    db = get_db()

    cursor = db.execute('SELECT * FROM programming_projects')

    intros = cursor.fetchall()
    # Retrieve the introduction from the database based on the intro_id
    # Render and return the template that displays the introduction

    # Generate the image source for the specific intro_id
    image_src = [url_for('static', filename=f'images/programming/{intro_id}.png')]

    file_path = image_src[0].lstrip('/')

    if os.path.exists(file_path)==False:
        image_src=['']

    # Store intro_id in session
    session['intro_id'] = intro_id

    return render_template('/programming projects/programming_projects.html',intro=intros[intro_id-1],image_srcs=image_src)


@app.route('/')
def home():
    return render_template('index.html',person=person)

@app.route('/trading')
def trading():

    return render_template('trading.html')

# Create a blueprint for the research sub-website
programming_bp=Blueprint('programming',__name__,url_prefix='/investment_research')

@programming_bp.route('/')
def programming():
    db = get_db()
    cursor = db.execute('SELECT * FROM programming_projects')
    intros = cursor.fetchall()
    session['intro_id'] = 0
    return render_template('investment_research.html',intros=intros)


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
    # db.create_all()
    if 'liveconsole' not in gethostname():
        # app.run()
        app.run(debug=True, port=3000)