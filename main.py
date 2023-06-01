import sqlite3 as sql
import tabulate as tb
from rich.markdown import Markdown
from rich.console import Console
from rich import print
import time

connection = sql.connect('TUTION_DB.sqlite')
cursor = connection.cursor()
console = Console()

# Course Table
cursor.execute('''CREATE TABLE IF NOT EXISTS COURSE
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                SUBJECTS TEXT NOT NULL);''')

# Student Table
cursor.execute('''CREATE TABLE IF NOT EXISTS STUDENT
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                AGE INTEGER NOT NULL,
                ADDRESS CHAR(50),
                PHONE CHAR(12),
                COURSE_ID INTEGER NOT NULL,
                FOREIGN KEY (COURSE_ID) REFERENCES COURSE(ID));''')

# Subject Table
cursor.execute('''CREATE TABLE IF NOT EXISTS SUBJECT
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                MANDATORY INTEGER NOT NULL);''')

# Teacher Table
cursor.execute('''CREATE TABLE IF NOT EXISTS TEACHER
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                AGE INTEGER NOT NULL,
                PHONE CHAR(12),
                SUBJECT_ID INTEGER NOT NULL,
                FOREIGN KEY (SUBJECT_ID) REFERENCES SUBJECT(ID));''')


def add_courses():
    MandatorySubjects = ['Math', 'English', "Skill Development"]
    NonMandatorySubjects = [
    "Physics", "Chemistry", "Biology",
    "History", "Geography", "Economics", "Civics",
    "Accountancy", "Business", "Commerce",
    "Computer Science", "Web Development", "Computer Engineering",
    "Data Science", "Artificial Intelligence", "Computer Graphics",
]

    courses = [
    ("Science course", [
        'Physics', 'Chemistry', "Biology"]),
    ("Social Science course", [
        'History', 'Geography', "Economics", "Civics"]),
    ("Foundation Commerce course", [
        'Accountancy', 'Business', "Commerce"]),
    ("Foundation Computer Science course", [
        "Computer Science", "Web Development", "Computer Engineering"]),
    ("Intermediate Computer Science course", [
        "Data Science", "Artificial Intelligence", "Computer Graphics"]),
]


    for i, subject in enumerate(MandatorySubjects):
        cursor.execute('''INSERT INTO SUBJECT(NAME,MANDATORY) VALUES (?,?)''',
                   (subject, 1))

    for i, subject in enumerate(NonMandatorySubjects):
        cursor.execute('''INSERT INTO SUBJECT(NAME,MANDATORY) VALUES (?,?)''',
                   (subject, 0))

    for name, subjects in courses:
        cursor.execute('''INSERT INTO COURSE(NAME,SUBJECTS) VALUES (?,?)''',
                   (name, ",".join(MandatorySubjects+subjects)))

cursor.execute("SELECT * FROM SUBJECT")
if len(cursor.fetchall()) == 0:
    add_courses()



def add_course():
    cursor = sql.connect('TUTION_DB.sqlite')
    name = input("Enter Course Name: ")
    subjects = input("Enter Course Subjects: ")
    cursor.execute('''INSERT INTO COURSE(NAME,SUBJECTS) VALUES (?,?)''',
                   (name, subjects))
    cursor.commit()


def add_subject():
    name = input("Enter Subject Name: ")
    mandatory = input("Is it mandatory? (y/n): ")
    if mandatory == 'y':
        mandatory = 1
    else:
        mandatory = 0
    cursor.execute('''INSERT INTO SUBJECT(NAME,MANDATORY) VALUES (?,?)''',
                   (name, mandatory))

    update()


def update():
    cursor.execute('''SELECT * FROM SUBJECT WHERE MANDATORY = 1''')
    mandatories = cursor.fetchall()
    cursor.execute('''SELECT * FROM COURSE''')
    courses = cursor.fetchall()

    for course in courses:
        for subject in mandatories:
            if subject[1] not in course[2].split(','):
                course[2] += "," + subject[1]
                cursor.execute('''UPDATE COURSE SET SUBJECTS = ? WHERE ID = ?''',
                               (course[2], course[0]))

    cursor.commit()

def show_teacher():
    cursor.execute('''SELECT * FROM TEACHER''')
    teachers = cursor.fetchall()
    if teachers is None:
        print("No teachers [red]available[/red]")
        return
    print("Printing all the available teachers...\n")
    print(tb.tabulate(teachers, headers=[
          'ID', 'Name', 'Age', 'Phone', 'Subject ID']))
    print("\n")
    time.sleep(5)
    main(section=1)


def add_teacher():
    print("Enter the teacher's name: ")
    name = input("> ")
    print(f"Enter the {name}'s age: ")
    age = int(input("> "))
    print(f"Enter the {name}'s phone number: ")
    phone = int(input("> "))
    subject_enquiry()
    print(f"Enter the subject id for {name}: ")
    subject_id = int(input("> "))
    cursor.execute('''INSERT INTO TEACHER(NAME,AGE,PHONE,SUBJECT_ID) VALUES (?,?,?,?)''',
              (name, age, phone, subject_id))
    connection.commit()
    print(f"Teacher {name} is added successfully into the database.\n")
    main(section=1)


def update_teacher():
    cursor.execute('''SELECT * FROM TEACHER''')
    if teachers:=cursor.fetchall() is None:
        print("No teachers available")
        return
    print("Printing all the available teachers...\n")
    print(tb.tabulate(teachers, headers=[
          'ID', 'Name', 'Age', 'Phone', 'Subject ID']))
    print("Enter the teacher's id to update: ")
    id = int(input("> "))
    print(f"Enter the teacher's phone number: ")
    phone = int(input("> "))
    subject_enquiry()
    print(f"Enter the subject id for teacher: ")
    subject_id = int(input("> "))
    cursor.execute('''UPDATE TEACHER SET PHONE = ?, SUBJECT_ID = ? WHERE ID = ?''',
              (phone, subject_id, id))
    connection.commit()
    print(f"Teacher {id} updated successfully in the database.\n")
    main(section=1)


def delete_teacher():
    cursor.execute('''SELECT * FROM TEACHER''')
    if cursor.fetchall() is None:
        print("No teachers available")
    print("Printing all the available teachers...\n")
    print(tb.tabulate(cursor.fetchall(), headers=[
          'ID', 'Name', 'Age', 'Phone', 'Subject ID']))
    print("Enter the teacher's id to delete: ")
    id = int(input("> "))
    cursor.execute('''DELETE FROM TEACHER WHERE ID = ?''', (id,))
    connection.commit()
    print(f"Teacher {id} deleted successfully in the database.\n")
    main(section=1)


def show_student():
    cursor.execute('''SELECT * FROM STUDENT''')
    if students:=cursor.fetchall() is None:
        print("No students available")
    print("Printing all the available students...\n")
    print(tb.tabulate(students(), headers=[
          'ID', 'Name', 'Age','Address' ,'Phone', 'Course ID']))
    print("\n")
    time.sleep(5)
    main(section=2)


def add_student():
    print("Enter the student's name: ")
    name = input("> ")
    print(f"Enter the {name}'s age: ")
    age = int(input("> "))
    print(f"Enter the {name}'s phone number: ")
    phone = int(input("> "))
    course_enquiry()
    print(f"Enter the course id for {name}: ")
    course_id = int(input("> "))
    cursor.execute('''INSERT INTO STUDENT(NAME,AGE,PHONE,COURSE_ID) VALUES (?,?,?,?)''',
              (name, age, phone, course_id))
    connection.commit()
    print(f"Student {name} is added successfully into the database.\n")
    main(section=2)


def update_student():
    cursor.execute('''SELECT * FROM STUDENT''')
    if cursor.fetchall() is None:
        print("No students available")
    print("Printing all the available students...\n")
    print(tb.tabulate(cursor.fetchall(), headers=[
          'ID', 'Name', 'Age', 'Phone', 'Course ID']))
    print("Enter the student's id to update: ")
    id = int(input("> "))
    print(f"Enter the student's phone number: ")
    phone = int(input("> "))
    course_enquiry()
    print(f"Enter the course id for student: ")
    course_id = int(input("> "))
    cursor.execute('''UPDATE STUDENT SET PHONE = ?, COURSE_ID = ? WHERE ID = ?''',
              (phone, course_id, id))
    connection.commit()
    print(f"Student {id} updated successfully in the database.\n")
    main(section=2)


def delete_student():
    cursor.execute('''SELECT * FROM STUDENT''')
    if cursor.fetchall() is None:
        print("No students available")
    print("Printing all the available students...\n")
    print(tb.tabulate(cursor.fetchall(), headers=[
          'ID', 'Name', 'Age', 'Phone', 'Course ID']))
    print("Enter the student's id to delete: ")
    id = int(input("> "))
    cursor.execute('''DELETE FROM STUDENT WHERE ID = ?''', (id,))
    connection.commit()
    print(f"Student {id} deleted successfully in the database.\n")
    main(section=2)


def course_enquiry():
    cursor.execute('''SELECT * FROM COURSE''')
    print("Printing all the available courses...\n")
    print(tb.tabulate(cursor.fetchall(), headers=['ID', 'Name', 'Subjects']))
    print("\n")
    time.sleep(5)


def subject_enquiry():
    cursor.execute('''SELECT ID,NAME FROM SUBJECT''')
    print("Printing all the available subjects...\n")
    print(tb.tabulate(cursor.fetchall(), headers=['ID', 'Name']))
    print("\n")
    time.sleep(5)

def sample():
    from faker import Faker

    fake = Faker()

    num_records = 10

    # fake teachers
    for _ in range(num_records):
        name = fake.name()
        age = fake.random_int(min=25, max=55)
        phone = f'+91 {fake.msisdn()[3:]}'
        subject_id = fake.random_int(min=1, max=19)

        cursor.execute('''INSERT INTO TEACHER (NAME, AGE, PHONE, SUBJECT_ID)
                        VALUES (?, ?, ?, ?)''', (name, age, phone, subject_id))

    connection.commit()

    # fake students
    for _ in range(num_records):
        name = fake.name()
        age = fake.random_int(min=18, max=25)
        address = fake.address().replace('\n', ', ')
        phone = f'+91 {fake.msisdn()[3:]}'
        course_id = fake.random_int(min=1, max=5)

        cursor.execute('''INSERT INTO STUDENT (NAME, AGE, ADDRESS, PHONE, COURSE_ID)
                        VALUES (?, ?, ?, ?, ?)''', (name, age, address, phone, course_id))

    connection.commit()


def main(section=None):
    if section is None:
        console.print(Markdown(open(r"menu\main_menu.md").read()))
        section = int(input("Enter in which sction you want to visit: "))

    match section:
        case 1:
            console.print(Markdown(open(r"menu\teacher_menu.md").read()))
            operation = int(
                input("Enter in which operation you want to perform: "))

            match operation:
                case 1:
                    show_teacher()
                case 2:
                    add_teacher()
                case 3:
                    update_teacher()
                case 4:
                    delete_teacher()
                case 5:
                    main()
                case _:
                    print("Invalid operation")
                    main(section=1)
        case 2:
            console.print(Markdown(open(r"menu\student_menu.md").read()))
            operation = int(
                input("Enter in which operation you want to perform: "))

            match operation:
                case 1:
                    show_student()
                case 2:
                    add_student()
                case 3:
                    update_student()
                case 4:
                    delete_student()
                case 5:
                    main()
                case _:
                    print("Invalid operation")
                    main(section=2)
        case 3:
            console.print(Markdown(open(r"menu\course_menu.md").read()))
            operation = int(
                input("Enter in which operation you want to perform: "))

            match operation:
                case 1:
                    subject_enquiry()
                    main(section=3)
                case 2:
                    add_subject()
                    main(section=3)
                case 3:
                    course_enquiry()
                    main(section=3)
                case 4:
                    add_course()
                    main(section=3)
                case 5:
                    main()
                case _:
                    print("Invalid operation")
                    main(section=3)
        case 4:
            console.print(
                Markdown("## Thank you for using the Tution Management System"))

        case _:
            print("[bold red]Invalid[/bold red] section")
            main()

sample()
main()


connection.commit()
connection.close()
