import argparse
import sqlite3
from pathlib import Path

DATABASE = 'test.db'

DEFAULT_PROFILE = {
    'name': 'YANG Zeshi, Ph.D.',
    'headline': 'VC Analyst | Investment Research',
    'email': 'yangzeshi997@gmail.com',
    'phone': ' +(65) 89642663',
    'location': 'Singapore',
    'introduction': """
    <p>
    <strong>Welcome &mdash; I&rsquo;m YANG Zeshi, Ph.D.</strong>
    </p>

    <p>
    I am an Analyst at Reeknot Investment, focused on deeptech investment research and venture analysis.
    My training across mineral engineering, ferrous metallurgy, and mechanical engineering (B.Eng., M.Eng., Ph.D.) provides a rigorous foundation for technical diligence and investment decision support.
    </p>

    <p>
    My publicly shareable work includes technical due diligence on operating companies, sell-side deal sourcing support for portfolio companies, strategic research on Singapore&rsquo;s role in global trade, startup qualitative due diligence through events and programs, and AI-enabled automation for internal research workflows.
    </p>

    <p>
    <strong>Current focus</strong><br>
    I currently focus on evaluating scalable deeptech businesses through structured technical, strategic, and market analysis, with an emphasis on long-term value creation.
    </p>

    <p>
    <em>I welcome discussion with founders, operators, and investors on deeptech investing, technical diligence, and research system design. You can reach me via <a href="mailto:yangzeshi997@gmail.com">email</a> or <a href="https://www.linkedin.com/in/zeshi-yang">LinkedIn</a>.</em>
    </p>
    """,
}

SECTION_TABLES = {
    'investment': 'programming_projects',
    'academic': 'research_projects',
}


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_site_profile_table(conn):
    conn.execute(
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

    row = conn.execute('SELECT id FROM site_profile WHERE id = 1').fetchone()
    if row is None:
        conn.execute(
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
    conn.commit()


def read_optional_file(path_value):
    if not path_value:
        return None
    path = Path(path_value)
    return path.read_text(encoding='utf-8')


def profile_show(_args):
    with get_db() as conn:
        ensure_site_profile_table(conn)
        row = conn.execute('SELECT * FROM site_profile WHERE id = 1').fetchone()

    for key in ['name', 'headline', 'email', 'phone', 'location']:
        print(f'{key}: {row[key]}')
    print('introduction:')
    print(row['introduction'])


def profile_update(args):
    with get_db() as conn:
        ensure_site_profile_table(conn)
        row = conn.execute('SELECT * FROM site_profile WHERE id = 1').fetchone()

        introduction = read_optional_file(args.introduction_file)
        if introduction is None and args.introduction is not None:
            introduction = args.introduction

        values = {
            'name': args.name if args.name is not None else row['name'],
            'headline': args.headline if args.headline is not None else row['headline'],
            'email': args.email if args.email is not None else row['email'],
            'phone': args.phone if args.phone is not None else row['phone'],
            'location': args.location if args.location is not None else row['location'],
            'introduction': introduction if introduction is not None else row['introduction'],
        }

        conn.execute(
            '''
            UPDATE site_profile
            SET name = ?, headline = ?, email = ?, phone = ?, location = ?, introduction = ?
            WHERE id = 1
            ''',
            (
                values['name'],
                values['headline'],
                values['email'],
                values['phone'],
                values['location'],
                values['introduction'],
            ),
        )
        conn.commit()

    print('Profile updated.')


def project_list(args):
    table = SECTION_TABLES[args.section]
    with get_db() as conn:
        rows = conn.execute(
            f'SELECT id, title, full_title FROM {table} ORDER BY id'
        ).fetchall()

    for row in rows:
        print(f"{row['id']}: {row['title']} -> {row['full_title']}")


def project_edit(args):
    table = SECTION_TABLES[args.section]
    with get_db() as conn:
        row = conn.execute(
            f'SELECT * FROM {table} WHERE id = ?',
            (args.id,),
        ).fetchone()

        if row is None:
            raise SystemExit(f'Project id {args.id} not found in {table}.')

        content_from_file = read_optional_file(args.content_file)
        content_value = content_from_file if content_from_file is not None else args.content

        values = {
            'title': args.title if args.title is not None else row['title'],
            'full_title': args.full_title if args.full_title is not None else row['full_title'],
            'content': content_value if content_value is not None else row['content'],
        }

        conn.execute(
            f'UPDATE {table} SET title = ?, full_title = ?, content = ? WHERE id = ?',
            (values['title'], values['full_title'], values['content'], args.id),
        )
        conn.commit()

    print('Project updated.')


def build_parser():
    parser = argparse.ArgumentParser(description='Manage website content in test.db')
    subparsers = parser.add_subparsers(required=True)

    profile_parser = subparsers.add_parser('profile', help='Manage profile content')
    profile_subparsers = profile_parser.add_subparsers(required=True)

    profile_show_parser = profile_subparsers.add_parser('show', help='Show profile')
    profile_show_parser.set_defaults(func=profile_show)

    profile_update_parser = profile_subparsers.add_parser('update', help='Update profile')
    profile_update_parser.add_argument('--name')
    profile_update_parser.add_argument('--headline')
    profile_update_parser.add_argument('--email')
    profile_update_parser.add_argument('--phone')
    profile_update_parser.add_argument('--location')
    profile_update_parser.add_argument('--introduction')
    profile_update_parser.add_argument('--introduction-file')
    profile_update_parser.set_defaults(func=profile_update)

    project_parser = subparsers.add_parser('project', help='Manage project records')
    project_subparsers = project_parser.add_subparsers(required=True)

    project_list_parser = project_subparsers.add_parser('list', help='List projects')
    project_list_parser.add_argument('--section', choices=sorted(SECTION_TABLES), required=True)
    project_list_parser.set_defaults(func=project_list)

    project_edit_parser = project_subparsers.add_parser('edit', help='Edit a project')
    project_edit_parser.add_argument('--section', choices=sorted(SECTION_TABLES), required=True)
    project_edit_parser.add_argument('--id', type=int, required=True)
    project_edit_parser.add_argument('--title')
    project_edit_parser.add_argument('--full-title', dest='full_title')
    project_edit_parser.add_argument('--content')
    project_edit_parser.add_argument('--content-file')
    project_edit_parser.set_defaults(func=project_edit)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
