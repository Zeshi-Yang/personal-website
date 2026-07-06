# Python
import os
import smtplib
import sqlite3
from functools import wraps
from pathlib import Path
from socket import gethostname
from uuid import uuid4
from datetime import datetime
from email.message import EmailMessage

from flask import (
    Flask,
    Blueprint,
    abort,
    current_app,
    g,
    redirect,
    render_template,
    render_template_string,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

DATABASE = 'test.db'
ADMIN_PASSWORD_ENV = 'SITE_ADMIN_PASSWORD'
SMTP_HOST_ENV = 'SMTP_HOST'
SMTP_PORT_ENV = 'SMTP_PORT'
SMTP_USER_ENV = 'SMTP_USER'
SMTP_PASS_ENV = 'SMTP_PASS'
SMTP_FROM_ENV = 'SMTP_FROM'
CONTACT_NOTIFY_TO_ENV = 'CONTACT_NOTIFY_TO'
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}

ABOUT_INTRODUCTION = """
    <p>
    <strong>Professional profile</strong>
    </p>

    <p>
    I work across deeptech investment research, technical diligence, and AI-assisted research systems.
    My training in mineral engineering, metallurgy, and mechanical engineering gives me a technical base for reviewing industrial technology, manufacturing risk, and scale-up questions.
    </p>

    <p>
    My work connects company analysis, market research, and engineering evidence.
    I am interested in businesses where technical performance, production readiness, and commercial adoption need to be evaluated together.
    </p>

    <p>
    <strong>Current focus</strong><br>
    I focus on deeptech sectors including advanced manufacturing, AI infrastructure, robotics, industrial software, semiconductors, climate technology, and digital infrastructure.
    </p>

    <p>
    <em>I welcome discussion with founders, operators, and investors on deeptech investing, technical diligence, and research system design. You can reach me via <a href=\"mailto:yangzeshi997@gmail.com\">email</a> or <a href=\"https://www.linkedin.com/in/zeshi-yang\">LinkedIn</a>.</em>
    </p>
    """

DEFAULT_PROFILE = {
    'name': 'YANG Zeshi, Ph.D.',
    'headline': 'Deeptech VC Analyst | Technical Diligence',
    'email': 'yangzeshi997@gmail.com',
    'phone': ' +(65) 89642663',
    'location': 'Singapore',
    'introduction': ABOUT_INTRODUCTION,
}

# Add a new tab later by adding one entry here and creating corresponding routes/templates.
PROJECT_SECTIONS = {
    'academic': {
        'table': 'research_projects',
        'label': 'Academic Research',
        'legacy_image_dir': 'research',
    },
    'investment': {
        'table': 'programming_projects',
        'label': 'Investment Research',
        'legacy_image_dir': 'programming',
    },
}

AI_PROJECTS = [
    {
        'id': 'investment-research-hub',
        'category': 'Investment research',
        'name': 'Investment Research Hub',
        'image': 'images/ai_projects/screenshots/investment-research-hub.png',
        'summary': 'Private deployable library for investment artifacts, startup diligence, and source traceability.',
        'description': (
            'The hub is the strongest public-facing AI project because it sits directly on top of the investment workflow. The live app presents '
            'a single workbench for startup diligence, technical diligence projects, knowledge-tree projects, artifact previews, downloads, and source boundaries.'
        ),
        'details': [
            'Observed live sections for Startup DD, TDD Project, and KT Project, with 7 targets, 7 startup-DD items, 7 analysis versions, and 84 artifacts.',
            'Designed around source traceability: artifacts, source files, previews, downloads, and project links stay together.',
            'The page states a local-first privacy boundary, which fits research work that may include private diligence material.',
        ],
    },
    {
        'id': 'tdd-management-system',
        'category': 'Technical diligence',
        'name': 'TDD Management System',
        'image': 'images/ai_projects/screenshots/tdd-management-system.png',
        'summary': 'Technical diligence workbench for company records, claims, references, architecture notes, and investment judgment.',
        'description': (
            'This app translates technical diligence into a reviewable pipeline. The live page is built around company records, review status, '
            'technical thesis inspection, references, architecture notes, and investor-ready judgment.'
        ),
        'details': [
            'Observed live copy describes a startup technical due diligence system with faster navigation and tighter investor-ready signal.',
            'The empty-state guidance tells the user to inspect a company record with references, architecture notes, and investment judgment.',
            'Useful for deeptech deals where the technical claim, commercial implication, and evidence quality need to be reviewed together.',
        ],
    },
    {
        'id': 'startup-wiki',
        'category': 'VC sourcing',
        'name': 'Sourcing Wiki',
        'image': 'images/ai_projects/screenshots/startup-wiki.png',
        'summary': 'Startup and investor sourcing desk with QA signals, source checks, filters, and shortlist rotation.',
        'description': (
            'The Sourcing Wiki supports the front end of investment work: finding, checking, filtering, and rotating startup or investor candidates. '
            'It is less about writing a memo and more about keeping the sourcing funnel inspectable.'
        ),
        'details': [
            'Observed live dashboard copy for startup and investor review, QA, source checks, and shortlist rotation.',
            'Workflow starts from QA signals and active filters, then moves into review, data health, or search.',
            'Fits the same sourcing and screening need as the Investment Research page, but at the entity-knowledge level.',
        ],
    },
    {
        'id': 'artifact-hub',
        'category': 'Research artifacts',
        'name': 'Artifact Hub',
        'image': 'images/ai_projects/screenshots/artifact-hub.png',
        'summary': 'Local knowledge-ops library for generated deliverables, source-linked files, and reusable research artifacts.',
        'description': (
            'Artifact Hub is the file and metadata layer behind generated research work. It stores deliverables with summaries, tags, workstreams, '
            'status, source IDs, checksums, paths, and related files so generated outputs do not disappear into loose folders.'
        ),
        'details': [
            'Observed live app copy: one place for generated deliverables, source-linked files, and reusable artifacts.',
            'The API showed 4 indexed artifacts, including an expert-team operating layer and a Southeast Asia energy-system market map.',
            'Useful when agent-generated research needs provenance, versioning, and a stable retrieval surface.',
        ],
    },
    {
        'id': 'hermes-artifact-bridge',
        'category': 'Agent workflow',
        'name': 'Hermes Artifact Bridge',
        'image': 'images/ai_projects/screenshots/hermes-artifact-bridge.png',
        'summary': 'Live progress layer for long-running agent work, task history, status, and generated artifact links.',
        'description': (
            'Hermes Artifact Bridge makes background research operations visible. The live API exposes task status, progress, timestamps, steps, links, '
            'and event history, while the page keeps active work upfront and older work in a compact archive.'
        ),
        'details': [
            'Observed live task data with status, progress, steps, tags, generated links, and event messages.',
            'Designed for workflows that last longer than a single browser session and need resumable status.',
            'Pairs naturally with Artifact Hub: one layer tracks work progress, the other stores final outputs.',
        ],
    },
    {
        'id': 'sea-energy-systems',
        'category': 'Sector research',
        'name': 'SEA Energy Systems',
        'image': 'images/ai_projects/screenshots/sea-energy-systems.png',
        'summary': 'Study atlas for Southeast Asia energy systems before investor mapping.',
        'description': (
            'This sector atlas turns an energy research folder into a readable study surface. The live app frames Southeast Asia energy transition '
            'as a system-enablement problem, not a simple renewables list, which is the right level for investment mapping.'
        ),
        'details': [
            'Observed live modes for answer, presentation, study map, reader, sources, and next work.',
            'Current working answer starts from demand growth, fossil/import exposure, grids, financeability, regulation, and country differences.',
            'Relevant to climate-tech and infrastructure research where system context matters before company selection.',
        ],
    },
    {
        'id': 'knowledge-trees',
        'category': 'Learning systems',
        'name': 'Knowledge Trees',
        'image': 'images/ai_projects/screenshots/knowledge-trees.png',
        'summary': 'Concept-learning trees for VC, physical AI, data centers, robotics, software, and first principles.',
        'description': (
            'Knowledge Trees are structured learning maps for technical and investment concepts. The live app lists multiple trees, including VC 101, '
            'physical AI, first-principles concepts, software engineering, data centers, industrial AI, and robotics.'
        ),
        'details': [
            'Observed API metadata for VC 101 as a source-backed VC fundamentals map covering rounds, preferred stock, ownership, valuation, agency risk, and diligence lenses.',
            'Observed physical-AI tree metadata for embodied AI, robots, drones, equipment, factories, field operations, deployment safety, and operational diligence lenses.',
            'Useful for building repeatable technical context before evaluating deeptech companies.',
        ],
    },
    {
        'id': 'knowledge-mine',
        'category': 'Knowledge base',
        'name': 'Knowledge Mine',
        'image': 'images/ai_projects/screenshots/knowledge-mine.png',
        'summary': 'Topic-folder browser across incoming, raw, wiki, and derived materials.',
        'description': (
            'Knowledge Mine is an external-source-first research compiler. The live page presents a calmer dashboard for search, mines/library, sources, '
            'wiki pages, derived outputs, graph discovery, and source gaps.'
        ),
        'details': [
            'Observed live copy for source-first research: search, open active mines, inspect chronology, graph links, source gaps, and canonical wiki pages.',
            'Keeps incoming material, raw notes, wiki pages, and derived outputs separate instead of mixing evidence and synthesis.',
            'Supports the same source-separation discipline needed in investment memos and technical diligence.',
        ],
    },
    {
        'id': 'ai-capex-guidance-tracker',
        'category': 'AI infrastructure',
        'name': 'AI Capex Guidance Tracker',
        'image': 'images/ai_projects/screenshots/ai-capex-guidance-tracker.png',
        'summary': 'Analyst dashboard for AI infrastructure capex, guidance, evidence anchors, and review blockers.',
        'description': (
            'This is an investment-research tracker for AI infrastructure spending. The live app is organized around dashboard, compare, evidence, '
            'and review-queue views, turning scattered public-company disclosures into a cleaner peer-comparison workflow.'
        ),
        'details': [
            'Tracks capex, capex guidance, revenue or sales outlooks, source IDs, evidence anchors, and unresolved review blockers.',
            'Live page states that verified coverage currently stops at 2026-05-15, which prevents stale refresh dates from being mistaken for new evidence.',
            'Includes source links such as SEC company-facts data and evidence pages for individual company claims.',
        ],
    },
    {
        'id': 'ai-career-operations-tracker',
        'category': 'Career operations',
        'name': 'AI Career Operations Tracker',
        'image': 'images/ai_projects/ai-career-operations-tracker-public.svg',
        'summary': 'Turns role search rules, fit scoring, skip memory, and interview prep into a workflow.',
        'description': (
            'This is a private workflow system built from the local job-search tracker folder. It applies the same evidence discipline to career search: '
            'define a target role universe, score fit, track applications, remember skips, and generate dated watch reports.'
        ),
        'details': [
            'Local tracker currently holds 26 opportunities, 6 application records, and 3 dated reports.',
            'Search criteria prioritize VC/PE, deeptech, AI infrastructure, semiconductors, advanced manufacturing, robotics, climate tech, digital infrastructure, and industrial software.',
            'The public image is a sanitized preview because the real dashboard contains private application records.',
        ],
    },
]

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'my_secret_key'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        ensure_content_schema(g.db)

    return g.db


@app.teardown_appcontext
def close_connection(_exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def column_exists(db, table_name, column_name):
    columns = db.execute(f'PRAGMA table_info({table_name})').fetchall()
    return any(column['name'] == column_name for column in columns)


def ensure_site_profile_table(db):
    db.execute(
        '''
        CREATE TABLE IF NOT EXISTS site_profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT NOT NULL,
            headline TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            introduction TEXT NOT NULL
        )
        '''
    )

    existing = db.execute('SELECT id FROM site_profile WHERE id = 1').fetchone()
    if existing is None:
        db.execute(
            '''
            INSERT INTO site_profile
            (id, name, headline, email, phone, location, introduction)
            VALUES (1, ?, ?, ?, ?, ?, ?)
            ''',
            (
                DEFAULT_PROFILE['name'],
                DEFAULT_PROFILE['headline'],
                DEFAULT_PROFILE['email'],
                DEFAULT_PROFILE['phone'],
                DEFAULT_PROFILE['location'],
                DEFAULT_PROFILE['introduction'],
            ),
        )


def ensure_project_order_columns(db):
    for config in PROJECT_SECTIONS.values():
        table = config['table']
        if not column_exists(db, table, 'display_order'):
            db.execute(f'ALTER TABLE {table} ADD COLUMN display_order INTEGER')
        db.execute(f'UPDATE {table} SET display_order = id WHERE display_order IS NULL')


def ensure_project_images_table(db):
    db.execute(
        '''
        CREATE TABLE IF NOT EXISTS project_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            project_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            caption TEXT DEFAULT '',
            sort_order INTEGER NOT NULL DEFAULT 0
        )
        '''
    )
    db.execute(
        '''
        CREATE INDEX IF NOT EXISTS idx_project_images_section_project
        ON project_images(section, project_id, sort_order, id)
        '''
    )


def find_legacy_images(section, project_id):
    config = PROJECT_SECTIONS[section]
    legacy_dir = config['legacy_image_dir']
    folder = Path(app.root_path) / 'static' / 'images' / legacy_dir
    if not folder.exists():
        return []

    matches = []
    patterns = [f'{project_id}.*', f'{project_id}-*.*', f'{project_id}_*.*']
    seen = set()

    for pattern in patterns:
        for file_path in sorted(folder.glob(pattern)):
            if file_path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
                continue
            if file_path.name in seen:
                continue
            seen.add(file_path.name)
            matches.append(f'images/{legacy_dir}/{file_path.name}')

    return matches


def seed_legacy_project_images(db):
    for section, config in PROJECT_SECTIONS.items():
        table = config['table']
        projects = db.execute(f'SELECT id FROM {table}').fetchall()

        for project in projects:
            project_id = project['id']
            image_exists = db.execute(
                'SELECT 1 FROM project_images WHERE section = ? AND project_id = ? LIMIT 1',
                (section, project_id),
            ).fetchone()
            if image_exists is not None:
                continue

            legacy_paths = find_legacy_images(section, project_id)
            for idx, image_path in enumerate(legacy_paths, start=1):
                db.execute(
                    '''
                    INSERT INTO project_images (section, project_id, image_path, caption, sort_order)
                    VALUES (?, ?, ?, '', ?)
                    ''',
                    (section, project_id, image_path, idx),
                )


def apply_copy_quality_fixes(db):
    """Keep legacy seeded content aligned with the public credibility baseline."""
    db.execute(
        "UPDATE site_profile SET headline = ? WHERE headline = ?",
        ('Deeptech VC Analyst | Technical Diligence', 'VC Analyst | Investment Research'),
    )
    db.execute(
        "UPDATE site_profile SET introduction = REPLACE(introduction, ?, ?) WHERE introduction LIKE ?",
        ('Reeknot Investment', 'Reefknot Investment', '%Reeknot Investment%'),
    )
    db.execute(
        "UPDATE site_profile SET introduction = REPLACE(introduction, ?, ?) WHERE introduction LIKE ?",
        (
            'I am an Analyst at Reefknot Investment, focused on deeptech investment research and venture analysis.',
            'I am an Analyst at Reefknot Investment, where I focus on deeptech investment research, technical diligence, and venture analysis.',
            '%I am an Analyst at Reefknot Investment, focused on deeptech investment research and venture analysis.%',
        ),
    )
    db.execute(
        "UPDATE site_profile SET introduction = REPLACE(introduction, ?, ?) WHERE introduction LIKE ?",
        (
            'provides a rigorous foundation for technical diligence and investment decision support.',
            'provides a rigorous foundation for evaluating technical risk and supporting investment decisions.',
            '%provides a rigorous foundation for technical diligence and investment decision support.%',
        ),
    )
    db.execute(
        "UPDATE site_profile SET introduction = REPLACE(introduction, ?, ?) WHERE introduction LIKE ?",
        (
            'My publicly shareable work includes technical due diligence on operating companies, sell-side deal sourcing support for portfolio companies, strategic research on Singapore&rsquo;s role in global trade, startup qualitative due diligence through events and programs, and AI-enabled automation for internal research workflows.',
            'My publicly shareable work spans technical due diligence on operating companies, sell-side sourcing support for portfolio companies, strategic research on Singapore&rsquo;s role in global trade, startup diligence through events and programs, and AI-enabled automation for internal research workflows.',
            '%My publicly shareable work includes technical due diligence on operating companies, sell-side deal sourcing support for portfolio companies, strategic research on Singapore&rsquo;s role in global trade, startup qualitative due diligence through events and programs, and AI-enabled automation for internal research workflows.%',
        ),
    )
    db.execute(
        "UPDATE site_profile SET introduction = REPLACE(introduction, ?, ?) WHERE introduction LIKE ?",
        (
            'I currently focus on evaluating scalable deeptech businesses through structured technical, strategic, and market analysis, with an emphasis on long-term value creation.',
            'I focus on evaluating scalable deeptech businesses through structured technical, strategic, and market analysis, with an emphasis on long-term value creation.',
            '%I currently focus on evaluating scalable deeptech businesses through structured technical, strategic, and market analysis, with an emphasis on long-term value creation.%',
        ),
    )
    db.execute(
        "UPDATE site_profile SET introduction = ? WHERE introduction LIKE ?",
        (ABOUT_INTRODUCTION, '%Reefknot Investment%'),
    )
    db.execute(
        "UPDATE programming_projects SET title = ? WHERE title = ?",
        ('Stock Screener', 'Stocker Screener'),
    )
    db.execute(
        "UPDATE research_projects SET title = ? WHERE title = ?",
        ('Acoustic Signal Emissions', 'Acoustic Singal Emissions'),
    )


def ensure_content_schema(db):
    db.executescript((Path(app.root_path) / 'schema.sql').read_text(encoding='utf-8'))
    ensure_site_profile_table(db)
    apply_copy_quality_fixes(db)
    ensure_project_order_columns(db)
    ensure_project_images_table(db)
    seed_legacy_project_images(db)
    db.commit()


def get_site_profile():
    db = get_db()
    profile = db.execute('SELECT * FROM site_profile WHERE id = 1').fetchone()
    return profile


def section_config_or_404(section):
    config = PROJECT_SECTIONS.get(section)
    if config is None:
        abort(404)
    return config


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login', next=request.path))
        return view_func(*args, **kwargs)

    return wrapped


def get_project_images(section, project_id):
    db = get_db()
    rows = db.execute(
        '''
        SELECT id, image_path, caption, sort_order
        FROM project_images
        WHERE section = ? AND project_id = ?
        ORDER BY sort_order, id
        ''',
        (section, project_id),
    ).fetchall()

    images = []
    for row in rows:
        image_path = row['image_path']
        static_file = Path(app.root_path) / 'static' / image_path
        if static_file.exists() and static_file.is_file():
            images.append(row)

    return images


def image_urls_for_project(section, project_id):
    return [url_for('static', filename=row['image_path']) for row in get_project_images(section, project_id)]


def send_contact_notification_email(sender_email, audience, question):
    smtp_user = os.environ.get(SMTP_USER_ENV, '').strip()
    smtp_pass = os.environ.get(SMTP_PASS_ENV, '').strip()
    if not smtp_user or not smtp_pass:
        return False, 'Email notification is not configured (missing SMTP_USER/SMTP_PASS).'

    smtp_host = os.environ.get(SMTP_HOST_ENV, 'smtp.gmail.com').strip() or 'smtp.gmail.com'
    smtp_port_raw = os.environ.get(SMTP_PORT_ENV, '587').strip() or '587'
    try:
        smtp_port = int(smtp_port_raw)
    except ValueError:
        smtp_port = 587

    notify_to = os.environ.get(CONTACT_NOTIFY_TO_ENV, DEFAULT_PROFILE['email']).strip()
    from_email = os.environ.get(SMTP_FROM_ENV, smtp_user).strip() or smtp_user

    msg = EmailMessage()
    msg['Subject'] = f'New Contact Form Message ({audience})'
    msg['From'] = from_email
    msg['To'] = notify_to

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg.set_content(
        '\n'.join(
            [
                'A new message was submitted from your website contact form.',
                '',
                f'Time: {timestamp}',
                f'Audience: {audience}',
                f'Sender email: {sender_email}',
                '',
                'Message:',
                question,
            ]
        )
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=25) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True, None
    except Exception as exc:
        app.logger.exception('Failed to send contact notification email.')
        return False, str(exc)


def normalize_static_path(raw_path):
    cleaned = (raw_path or '').strip().lstrip('/')
    if cleaned.startswith('static/'):
        cleaned = cleaned[len('static/'):]

    candidate = Path(app.root_path) / 'static' / cleaned
    if candidate.exists() and candidate.is_file():
        return cleaned
    return None


def next_display_order(db, table):
    row = db.execute(f'SELECT COALESCE(MAX(display_order), 0) AS max_order FROM {table}').fetchone()
    return int(row['max_order']) + 1


def swap_project_order(db, table, project_id, direction):
    ordered = db.execute(
        f'SELECT id, display_order FROM {table} ORDER BY display_order, id'
    ).fetchall()

    index = next((i for i, row in enumerate(ordered) if row['id'] == project_id), None)
    if index is None:
        return False

    if direction == 'up' and index > 0:
        other = ordered[index - 1]
    elif direction == 'down' and index < len(ordered) - 1:
        other = ordered[index + 1]
    else:
        return False

    current = ordered[index]
    db.execute(
        f'UPDATE {table} SET display_order = ? WHERE id = ?',
        (other['display_order'], current['id']),
    )
    db.execute(
        f'UPDATE {table} SET display_order = ? WHERE id = ?',
        (current['display_order'], other['id']),
    )
    return True


def swap_image_order(db, section, project_id, image_id, direction):
    ordered = db.execute(
        '''
        SELECT id, sort_order
        FROM project_images
        WHERE section = ? AND project_id = ?
        ORDER BY sort_order, id
        ''',
        (section, project_id),
    ).fetchall()

    index = next((i for i, row in enumerate(ordered) if row['id'] == image_id), None)
    if index is None:
        return False

    if direction == 'up' and index > 0:
        other = ordered[index - 1]
    elif direction == 'down' and index < len(ordered) - 1:
        other = ordered[index + 1]
    else:
        return False

    current = ordered[index]
    db.execute(
        'UPDATE project_images SET sort_order = ? WHERE id = ?',
        (other['sort_order'], current['id']),
    )
    db.execute(
        'UPDATE project_images SET sort_order = ? WHERE id = ?',
        (current['sort_order'], other['id']),
    )
    return True


# Create a blueprint for the research sub-website
research_bp = Blueprint('research', __name__, url_prefix='/academic_research')


@research_bp.route('/')
def research():
    db = get_db()
    intros = db.execute(
        'SELECT * FROM research_projects ORDER BY display_order, id'
    ).fetchall()
    session['intro_id'] = 0
    return render_template('academic_research.html', intros=intros)


@app.context_processor
def inject_intros():
    db = get_db()
    research_intros = db.execute(
        'SELECT * FROM research_projects ORDER BY display_order, id'
    ).fetchall()
    programming_intros = db.execute(
        'SELECT * FROM programming_projects ORDER BY display_order, id'
    ).fetchall()

    intro_id = session.get('intro_id')

    return dict(
        research_intros=research_intros,
        programming_intros=programming_intros,
        intro_id=intro_id,
        current_year=datetime.now().year,
    )


@app.route('/academic_research/<int:intro_id>')
def show_intro_1(intro_id):
    db = get_db()
    intro = db.execute('SELECT * FROM research_projects WHERE id = ?', (intro_id,)).fetchone()
    if intro is None:
        abort(404)

    session['intro_id'] = intro_id
    image_srcs = image_urls_for_project('academic', intro_id)

    return render_template('/research projects/research_projects.html', intro=intro, image_srcs=image_srcs)


@app.route('/investment_research/<int:intro_id>')
def show_intro_2(intro_id):
    db = get_db()
    intro = db.execute('SELECT * FROM programming_projects WHERE id = ?', (intro_id,)).fetchone()
    if intro is None:
        abort(404)

    session['intro_id'] = intro_id
    image_srcs = image_urls_for_project('investment', intro_id)

    return render_template('/programming projects/programming_projects.html', intro=intro, image_srcs=image_srcs)


@app.route('/')
def home():
    person = get_site_profile()
    return render_template(
        'index.html',
        person=person,
    )


@app.route('/about')
def about():
    person = get_site_profile()
    return render_template('about.html', person=person)


@app.route('/ai_projects')
def ai_projects():
    return render_template('ai_projects.html', projects=AI_PROJECTS, selected_project=None)


@app.route('/ai_projects/<project_id>')
def show_ai_project(project_id):
    project = next((item for item in AI_PROJECTS if item['id'] == project_id), None)
    if project is None:
        abort(404)
    return render_template('ai_projects.html', projects=AI_PROJECTS, selected_project=project)


@app.route('/trading')
def trading():
    return abort(404)


# Create a blueprint for the research sub-website
programming_bp = Blueprint('programming', __name__, url_prefix='/investment_research')


@programming_bp.route('/')
def programming():
    db = get_db()
    intros = db.execute(
        'SELECT * FROM programming_projects ORDER BY display_order, id'
    ).fetchall()
    session['intro_id'] = 0
    return render_template('investment_research.html', intros=intros)


@app.route('/contact')
def contact():
    person = get_site_profile()
    return render_template('contact.html', person=person)


@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        email = request.form['email']
        question = request.form['question']
        audience = request.form.get('audience', 'General')
        tagged_question = f'[{audience}] {question}'

        db = get_db()
        db.execute('INSERT INTO contact (email, question) VALUES (?, ?)', (email, tagged_question))
        db.commit()

        notified, notify_error = send_contact_notification_email(email, audience, question)
        if notified:
            alert_message = 'Form submitted successfully. I have been notified by email.'
        elif notify_error and 'not configured' in notify_error:
            alert_message = 'Form submitted successfully. Email notification is not configured yet.'
        else:
            alert_message = 'Form submitted successfully, but email notification failed.'

        return render_template_string(
            '''
            <script>
                alert({{ alert_message|tojson }});
                window.history.back();
            </script>
            ''',
            alert_message=alert_message,
        )


@app.route('/admin')
def admin_home():
    return redirect(url_for('admin_profile'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    admin_password = os.environ.get(ADMIN_PASSWORD_ENV)

    if request.method == 'POST':
        posted_password = request.form.get('password', '')
        if not admin_password:
            error = f'Environment variable {ADMIN_PASSWORD_ENV} is not set on this machine.'
        elif posted_password != admin_password:
            error = 'Invalid password.'
        else:
            session['is_admin'] = True
            next_url = request.args.get('next') or url_for('admin_profile')
            return redirect(next_url)

    return render_template(
        'admin_login.html',
        error=error,
        password_configured=bool(admin_password),
        password_env=ADMIN_PASSWORD_ENV,
    )


@app.route('/admin/logout')
@admin_required
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))


@app.route('/admin/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():
    db = get_db()

    if request.method == 'POST':
        db.execute(
            '''
            UPDATE site_profile
            SET name = ?, headline = ?, email = ?, phone = ?, location = ?, introduction = ?
            WHERE id = 1
            ''',
            (
                request.form.get('name', '').strip(),
                request.form.get('headline', '').strip(),
                request.form.get('email', '').strip(),
                request.form.get('phone', '').strip(),
                request.form.get('location', '').strip(),
                request.form.get('introduction', '').strip(),
            ),
        )
        db.commit()
        return redirect(url_for('admin_profile', saved='1'))

    profile = db.execute('SELECT * FROM site_profile WHERE id = 1').fetchone()
    return render_template('admin_profile.html', profile=profile, saved=request.args.get('saved') == '1')


@app.route('/admin/projects/<section>')
@admin_required
def admin_projects(section):
    config = section_config_or_404(section)
    db = get_db()

    projects = db.execute(
        f'''
        SELECT p.id, p.title, p.full_title, p.display_order,
               (
                   SELECT image_path
                   FROM project_images pi
                   WHERE pi.section = ? AND pi.project_id = p.id
                   ORDER BY pi.sort_order, pi.id
                   LIMIT 1
               ) AS first_image,
               (
                   SELECT COUNT(*)
                   FROM project_images pi
                   WHERE pi.section = ? AND pi.project_id = p.id
               ) AS image_count
        FROM {config['table']} p
        ORDER BY p.display_order, p.id
        ''',
        (section, section),
    ).fetchall()

    return render_template(
        'admin_project_list.html',
        section=section,
        section_label=config['label'],
        projects=projects,
        created=request.args.get('created') == '1',
    )


@app.route('/admin/projects/<section>/new', methods=['POST'])
@admin_required
def admin_new_project(section):
    config = section_config_or_404(section)
    db = get_db()

    title = request.form.get('title', '').strip()
    full_title = request.form.get('full_title', '').strip()
    content = request.form.get('content', '').strip()

    if not title:
        title = 'New Project'
    if not full_title:
        full_title = title
    if not content:
        content = '<p>Content coming soon.</p>'

    display_order = next_display_order(db, config['table'])
    cursor = db.execute(
        f'''
        INSERT INTO {config['table']} (title, full_title, content, display_order)
        VALUES (?, ?, ?, ?)
        ''',
        (title, full_title, content, display_order),
    )
    db.commit()

    return redirect(
        url_for('admin_edit_project', section=section, project_id=cursor.lastrowid, created='1')
    )


@app.route('/admin/projects/<section>/<int:project_id>/move/<direction>', methods=['POST'])
@admin_required
def admin_move_project(section, project_id, direction):
    config = section_config_or_404(section)
    if direction not in {'up', 'down'}:
        abort(404)

    db = get_db()
    swapped = swap_project_order(db, config['table'], project_id, direction)
    if swapped:
        db.commit()

    return redirect(url_for('admin_projects', section=section))


@app.route('/admin/projects/<section>/<int:project_id>/delete', methods=['POST'])
@admin_required
def admin_delete_project(section, project_id):
    config = section_config_or_404(section)
    db = get_db()

    db.execute(f'DELETE FROM {config["table"]} WHERE id = ?', (project_id,))

    image_rows = db.execute(
        'SELECT image_path FROM project_images WHERE section = ? AND project_id = ?',
        (section, project_id),
    ).fetchall()
    for row in image_rows:
        image_path = row['image_path']
        if image_path.startswith(f'images/uploads/{section}/'):
            file_path = Path(app.root_path) / 'static' / image_path
            if file_path.exists():
                file_path.unlink()

    db.execute(
        'DELETE FROM project_images WHERE section = ? AND project_id = ?',
        (section, project_id),
    )
    db.commit()

    return redirect(url_for('admin_projects', section=section))


@app.route('/admin/projects/<section>/<int:project_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_project(section, project_id):
    config = section_config_or_404(section)
    db = get_db()

    project = db.execute(
        f'SELECT id, title, full_title, content, display_order FROM {config["table"]} WHERE id = ?',
        (project_id,),
    ).fetchone()

    if project is None:
        abort(404)

    if request.method == 'POST':
        db.execute(
            f'UPDATE {config["table"]} SET title = ?, full_title = ?, content = ? WHERE id = ?',
            (
                request.form.get('title', '').strip(),
                request.form.get('full_title', '').strip(),
                request.form.get('content', '').strip(),
                project_id,
            ),
        )
        db.commit()
        return redirect(url_for('admin_edit_project', section=section, project_id=project_id, saved='1'))

    images = get_project_images(section, project_id)
    image_view = [
        {
            'id': image['id'],
            'image_path': image['image_path'],
            'caption': image['caption'],
            'sort_order': image['sort_order'],
            'url': url_for('static', filename=image['image_path']),
        }
        for image in images
    ]

    return render_template(
        'admin_project_edit.html',
        section=section,
        section_label=config['label'],
        project=project,
        images=image_view,
        saved=request.args.get('saved') == '1',
        created=request.args.get('created') == '1',
        image_saved=request.args.get('image_saved') == '1',
        image_error=request.args.get('image_error', ''),
    )


@app.route('/admin/projects/<section>/<int:project_id>/images/add', methods=['POST'])
@admin_required
def admin_add_project_image(section, project_id):
    section_config_or_404(section)
    db = get_db()

    project_exists = db.execute(
        f'SELECT id FROM {PROJECT_SECTIONS[section]["table"]} WHERE id = ?',
        (project_id,),
    ).fetchone()
    if project_exists is None:
        abort(404)

    upload = request.files.get('image_file')
    manual_path = request.form.get('image_path', '').strip()
    caption = request.form.get('caption', '').strip()

    image_path = None

    if upload and upload.filename:
        suffix = Path(upload.filename).suffix.lower()
        if suffix not in ALLOWED_IMAGE_EXTENSIONS:
            return redirect(
                url_for(
                    'admin_edit_project',
                    section=section,
                    project_id=project_id,
                    image_error='Only png, jpg, jpeg, webp, and gif are supported.',
                )
            )

        filename = secure_filename(upload.filename)
        safe_name = f'{project_id}_{uuid4().hex[:10]}{Path(filename).suffix.lower()}'
        target_dir = Path(app.root_path) / 'static' / 'images' / 'uploads' / section
        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / safe_name
        upload.save(target_file)
        image_path = f'images/uploads/{section}/{safe_name}'
    elif manual_path:
        image_path = normalize_static_path(manual_path)
        if image_path is None:
            return redirect(
                url_for(
                    'admin_edit_project',
                    section=section,
                    project_id=project_id,
                    image_error='Static path not found. Use a valid file under /static.',
                )
            )
    else:
        return redirect(
            url_for(
                'admin_edit_project',
                section=section,
                project_id=project_id,
                image_error='Provide an upload file or a static image path.',
            )
        )

    row = db.execute(
        '''
        SELECT COALESCE(MAX(sort_order), 0) AS max_sort
        FROM project_images
        WHERE section = ? AND project_id = ?
        ''',
        (section, project_id),
    ).fetchone()
    next_sort = int(row['max_sort']) + 1

    db.execute(
        '''
        INSERT INTO project_images (section, project_id, image_path, caption, sort_order)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (section, project_id, image_path, caption, next_sort),
    )
    db.commit()

    return redirect(
        url_for('admin_edit_project', section=section, project_id=project_id, image_saved='1')
    )


@app.route('/admin/projects/<section>/<int:project_id>/images/<int:image_id>/move/<direction>', methods=['POST'])
@admin_required
def admin_move_project_image(section, project_id, image_id, direction):
    section_config_or_404(section)
    if direction not in {'up', 'down'}:
        abort(404)

    db = get_db()
    swapped = swap_image_order(db, section, project_id, image_id, direction)
    if swapped:
        db.commit()

    return redirect(url_for('admin_edit_project', section=section, project_id=project_id))


@app.route('/admin/projects/<section>/<int:project_id>/images/<int:image_id>/delete', methods=['POST'])
@admin_required
def admin_delete_project_image(section, project_id, image_id):
    section_config_or_404(section)
    db = get_db()

    row = db.execute(
        'SELECT image_path FROM project_images WHERE id = ? AND section = ? AND project_id = ?',
        (image_id, section, project_id),
    ).fetchone()
    if row is None:
        abort(404)

    image_path = row['image_path']
    if image_path.startswith(f'images/uploads/{section}/'):
        file_path = Path(app.root_path) / 'static' / image_path
        if file_path.exists():
            file_path.unlink()

    db.execute('DELETE FROM project_images WHERE id = ?', (image_id,))
    db.commit()

    return redirect(url_for('admin_edit_project', section=section, project_id=project_id))


@app.route('/test')
def test():
    return render_template('test.html')


# Register the blueprint
app.register_blueprint(research_bp)
app.register_blueprint(programming_bp)


if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run()
        # app.run(debug=True, port=3000)
