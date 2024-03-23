# TuitionDB

TuitionDB is a simple SQLite-based database management system for a tuition center. It allows you to manage courses, subjects, students, and teachers.

## Features

- Course Management: Add and view courses offered by the tuition center.
- Subject Management: Add and view subjects available for each course.
- Student Management: Add and view student details, including name, age, address, phone number, and enrolled course.
- Teacher Management: Add and view teacher details, including name, age, phone number, and assigned subject.

## Getting Started

To get started with the TUTION_DB project, follow these steps:

1. Clone the repository: `git clone https://github.com/KOMNOOB/TuitionDB.git`
2. Install the required dependencies: `pip install rich faker tabulate`
3. Run the application: `python main.py`

## Usage

Once the application is running, you can use the following commands to interact with the database:

- `add_course`: Add a new course to the database.
- `add_subject`: Add a new subject to the database.
- `add_student`: Add a new student to the database.
- `add_teacher`: Add a new teacher to the database.
- `view_courses`: View all the courses in the database.
- `view_subjects`: View all the subjects in the database.
- `view_students`: View all the students in the database.
- `view_teachers`: View all the teachers in the database.

## Database Schema

The database schema for the TUTION_DB project is as follows:

- COURSE: Holds information about the courses offered by the tuition center.
  - ID: Unique identifier for the course.
  - NAME: Name of the course.
  - SUBJECTS: Comma-separated list of subject names for the course.

- SUBJECT: Holds information about the subjects available for each course.
  - ID: Unique identifier for the subject.
  - NAME: Name of the subject.
  - MANDATORY: Indicates whether the subject is mandatory or not (1 for mandatory, 0 for non-mandatory).

- STUDENT: Holds information about the students enrolled in the tuition center.
  - ID: Unique identifier for the student.
  - NAME: Name of the student.
  - AGE: Age of the student.
  - ADDRESS: Address of the student.
  - PHONE: Phone number of the student.
  - COURSE_ID: Foreign key referencing the ID of the course the student is enrolled in.

- TEACHER: Holds information about the teachers in the tuition center.
  - ID: Unique identifier for the teacher.
  - NAME: Name of the teacher.
  - AGE: Age of the teacher.
  - PHONE: Phone number of the teacher.
  - SUBJECT_ID: Foreign key referencing the ID of the subject the teacher is assigned to.
