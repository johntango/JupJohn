# Here's that last version rewritten using Python objects.

def one(gen):
    return next(gen, None)

class Student:
    def __init__(self, sid, sname):
        self.id = sid
        self.name = sname

class Pset:
    def __init__(self, pid, points):
        self.id = pid
        self.points = points

class Grade:
    def __init__(self, sid, pid, points):
        self.student = sid
        self.pset = pid
        self.points = points

class Db:
    def __init__(self):
        self.students = []
        self.psets = []
        self.grades = []

    # Now notice that we are copying the old code _almost_ verbatim into the class body.
    # Only differences: using '.blah' instead of '["blah"]';
    #   using class constructors instead of dictionary literals;
    #   making calls within the class with [db.foo(...)] instead of [foo(db, ...)].

    # Add a new student to the database.
    def addStudent(db, student_id, student_name):
        db.students.append(Student(student_id, student_name))

    # Return the ID of the student with a given name, or None if that name isn't found.
    def studentIdFromName(db, student_name):
        return one(student.id
                   for student in db.students
                   if student.name == student_name)

    # Return the name of the student with a given ID, or None if that ID isn't found.
    def studentNameFromId(db, student_id):
        return one(student.name
                   for student in db.students
                   if student.id == student_id)

    # Add a new pset to the database.
    def addPset(db, pset_id, pset_total_points):
        db.psets.append(Pset(pset_id, pset_total_points))

    # Return the point value of the pset with a given ID, or None if that ID isn't found.
    def psetPointsFromId(db, pset_id):
        return one(pset.points
                   for pset in db.psets
                   if pset.id == pset_id)

    # Record a student's grade on a pset.
    def addGrade(db, student_id, pset_id, points):
        db.grades.append(Grade(student_id, pset_id, points))

    # Which grade did this student get on this pset?  (Returns None if no grade has been recorded.)
    def gradeOn(db, student_id, pset_id):
        return one(grade.points
                   for grade in db.grades
                   if grade.student == student_id
                   if grade.pset == pset_id)

    # Return all of a student's grades, as a dictionary from pset IDs to points.
    def studentGrades(db, student_id):
        return {grade.pset: grade.points
                for grade in db.grades
                if grade.student == student_id}

    # Return all grades on a pset, as a dictionary from student names to grades.
    # Notice that we're making it interesting by working with student names instead of IDs.
    # The grades table doesn't include student names directly!
    def gradesOnPset(self, pset_id):
        return {student.name: grade.points
                for grade in db.grades
                if grade.pset == pset_id
                for student in db.students
                if student.id == grade.student}

    def gradeOnWeighted(db, student_id, pset):
        grade = db.gradeOn(student_id, pset.id)
        if grade == None:
            return 0
        else:
            return grade * 1.0 / pset.points

    def studentGradesWeighted(db, student_id):
        return [db.gradeOnWeighted(student_id, pset)
                for pset in db.psets]

    def finalGradeOf(db, student_id):
        grades = db.studentGradesWeighted(student_id)
        return round(sum(grades) / len(grades) * 100, 1)

    def finalGrades(db):
        return [{"id": student.id,
                 "name": student.name,
                 "grade": db.finalGradeOf(student.id)}
                for student in db.students]

db = Db()

db.addStudent(1, "Alice")
db.addStudent(2, "Bob")
db.addStudent(3, "Charlie")

db.addPset(1, 10)
db.addPset(2, 20)
db.addPset(3, 30)

db.addGrade(1, 1, 10)
db.addGrade(1, 2, 18)
db.addGrade(1, 3, 25)
db.addGrade(2, 3, 15)
db.addGrade(3, 3, 10)

assert db.studentIdFromName("Bob") == 2
assert db.studentIdFromName("Doug") == None

assert db.studentNameFromId(3) == "Charlie"
assert db.studentNameFromId(4) == None

assert db.psetPointsFromId(2) == 20
assert db.psetPointsFromId(8) == None

assert db.gradeOn(1, 3) == 25
assert db.gradeOn(2, 1) == None

assert db.studentGrades(1) == {1: 10, 2: 18, 3: 25}

assert db.gradesOnPset(3) == {"Alice": 25, "Bob": 15, "Charlie": 10}

print (db.grades)

print (db.finalGrades())
