## A few generic functions for working with dictionaries and comprehensions

def one(gen):
    return next(gen, None)

def get(dict, key):
    if dict == None:
        return None
    elif key in dict:
        return dict[key]
    else:
        return None

def get2(dict1, key1, key2):
    dict2 = get(dict1, key1)
    if dict2:
        return get(dict2, key2)
    else:
        return None

def get3(dict1, key1, key2, key3):
    dict3 = get2(dict1, key1, key2)
    if dict3:
        return get(dict3, key3)
    else:
        return None

def get4(dict1, key1, key2, key3, key4):
    dict4 = get3(dict1, key1, key2, key3)
    if dict4:
        return get(dict4, key4)
    else:
        return None

def add2(dict1, key1, key2, value):
    if key1 not in dict1:
        dict1[key1] = {}

    dict1[key1][key2] = value


## We will tour through a series of representations of a grades database for a class much like this one.

# Create a new empty database.
def empty():
    return {"students": [],
            "psets": [],
            "grades": []}

# Add a new student to the database.
def addStudent(db, student_id, student_name):
    db["students"].append({"id": student_id,
                           "name": student_name})

# Return the ID of the student with a given name, or None if that name isn't found.
def studentIdFromName(db, student_name):
    return one(student["id"]
               for student in db["students"]
               if student["name"] == student_name)

# Return the name of the student with a given ID, or None if that ID isn't found.
def studentNameFromId(db, student_id):
    return one(student["name"]
               for student in db["students"]
               if student["id"] == student_id)

# Add a new pset to the database.
def addPset(db, pset_id, pset_total_points):
    db["psets"].append({"id": pset_id,
                        "points": pset_total_points})

# Return the point value of the pset with a given ID, or None if that ID isn't found.
def psetPointsFromId(db, pset_id):
    return one(pset["points"]
               for pset in db["psets"]
               if pset["id"] == pset_id)

# Record a student's grade on a pset.
def addGrade(db, student_id, pset_id, points):
    db["grades"].append({"student": student_id,
                         "pset": pset_id,
                         "points": points})

# Which grade did this student get on this pset?  (Returns None if no grade has been recorded.)
def gradeOn(db, student_id, pset_id):
    return one(grade["points"]
               for grade in db["grades"]
               if grade["student"] == student_id
               if grade["pset"] == pset_id)

# Return all of a student's grades, as a dictionary from pset IDs to points.
def studentGrades(db, student_id):
    return {grade["pset"]: grade["points"]
            for grade in db["grades"]
            if grade["student"] == student_id}

# Return all grades on a pset, as a dictionary from student names to grades.
# Notice that we're making it interesting by working with student names instead of IDs.
# The grades table doesn't include student names directly!
def gradesOnPset(db, pset_id):
    return {student["name"]: grade["points"]
            for grade in db["grades"]
            if grade["pset"] == pset_id
            for student in db["students"]
            if student["id"] == grade["student"]}

# OK, time for the fanciest report yet.
# Imagine it's the end of the semester, and the course staff need the final list of all scores for all students.
# The registrar wants this information as a spreadsheet that includes student IDs, names, and overall scores.
# However, the registrar doesn't want to hear anything about the details of which assignments there were.
# Let's assume that (1) psets are the only factor in grades and (2) each pset is weighted equally.

# To start with, let's implement a version of studentGrades that:
# (1) includes zeroes for missing grades,
# (2) divides by the point total for each pset, and
# (3) returns a list of scores.
# One more helper function is useful first.
def gradeOnWeighted(db, student_id, pset):
    grade = gradeOn(db, student_id, pset["id"])
    if grade == None:
        return 0
    else:
        return grade * 1.0 / pset["points"]
        # Note the multiplication by 1.0 to switch to using rational numbers and avoid rounding!
def studentGradesWeighted(db, student_id):
    return [gradeOnWeighted(db, student_id, pset)
            for pset in db["psets"]]

# Next, computing the final grade of a student.
def finalGradeOf(db, student_id):
    grades = studentGradesWeighted(db, student_id)
    return round(sum(grades) / len(grades) * 100, 1)

# Finally, computing for all students.
def finalGrades(db):
    return [{"id": student["id"],
             "name": student["name"],
             "grade": finalGradeOf(db, student["id"])}
            for student in db["students"]]

def tests():
    db = empty()

    addStudent(db, 1, "Alice")
    addStudent(db, 2, "Bob")
    addStudent(db, 3, "Charlie")

    addPset(db, 1, 10)
    addPset(db, 2, 20)
    addPset(db, 3, 30)

    addGrade(db, 1, 1, 10)
    addGrade(db, 1, 2, 18)
    addGrade(db, 1, 3, 25)
    addGrade(db, 2, 3, 15)
    addGrade(db, 3, 3, 10)

    assert studentIdFromName(db, "Bob") == 2
    assert studentIdFromName(db, "Doug") == None

    assert studentNameFromId(db, 3) == "Charlie"
    assert studentNameFromId(db, 4) == None

    assert psetPointsFromId(db, 2) == 20
    assert psetPointsFromId(db, 8) == None

    assert gradeOn(db, 1, 3) == 25
    assert gradeOn(db, 2, 1) == None

    assert studentGrades(db, 1) == {1: 10, 2: 18, 3: 25}

    assert gradesOnPset(db, 3) == {"Alice": 25, "Bob": 15, "Charlie": 10}

    print finalGrades(db)
