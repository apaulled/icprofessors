import json
import mysql.connector
from bson import ObjectId


def get_id_from_column(connection, table_name, column_name, entry):
    if isinstance(entry, str) and len(entry) == 0:
        return None

    curs = connection.cursor()
    curs.execute(f"select id from {table_name} where {column_name} = %s", (entry,))
    res = curs.fetchone()
    if res:
        return res[0]
    else:
        curs.execute(f"insert into {table_name} ({column_name}) values (%s)", (entry,))
        conn.commit()
        curs.execute(f"select id from {table_name} where {column_name} = %s", (entry,))
        res = curs.fetchone()
        return res[0]


def insert_fs(connection, curs, fac_id, spec):
    spec = spec.strip()
    spec_id = get_id_from_column(connection, 'specialties', 'name', spec)
    if spec_id is not None:
        curs.execute("insert into faculty_specialties (faculty_id, specialty_id) values (%s, %s)", (fac_id, spec_id))
        connection.commit()


def remove_bad_characters(s):
    return "".join(c for c in s if c.isalnum() or c == ' ')


password = ''
with open('passwords.json') as file:
    passwords = json.load(file)
    password = passwords['paul']

with open('lukas_faculty.json') as file:
    faculty = json.loads(file.read())

    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=password,
        password="704860125",
        database="faculty"
    )
    cursor = conn.cursor()

    for fac in faculty:
        _id = ObjectId(fac['_id']).binary
        name = fac.get('name')
        email = fac.get('Email')
        phone = fac.get('Phone')
        url = fac.get('url')

        office = fac.get('Office')
        school = fac.get('School')
        department = fac.get('department')
        department_section = fac.get('department section')
        job = fac.get('job')
        specialty_string = fac.get('Specialty')
        office_id = None
        school_id = None
        department_id = None
        department_section_id = None
        job_id = None

        if phone and len(phone) != 10:
            phone = "".join(c for c in phone if '1' <= c <= '9')

        if office:
            if 'Ithaca' in office:
                office = office.split(',')[0]
            office_id = get_id_from_column(conn, 'offices', 'location', office)

        if school:
            school_id = get_id_from_column(conn, 'schools', 'name', school)

        if department:
            department_id = get_id_from_column(conn, 'departments', 'name', department)

        if department_section:
            department_section_id = get_id_from_column(conn, 'department_sections', 'title', department_section)

        if job:
            job_id = get_id_from_column(conn, 'jobs', 'name', job)

        cursor.execute(
            """
            insert into faculty (id, name, email, phone, url, office_id, school_id, department_id, department_section_id, job_id) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (_id, name, email, phone, url, office_id, school_id, department_id, department_section_id, job_id)
        )
        conn.commit()

        if specialty_string:
            parts = specialty_string.split(',')
            for part in parts:
                if 'and' in part:
                    for p in part.split('and'):
                        insert_fs(conn, cursor, _id, p)
                elif '&' in part:
                    for p in part.split('&'):
                        insert_fs(conn, cursor, _id, p)
                else:
                    insert_fs(conn, cursor, _id, part)
