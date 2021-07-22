

## Version #2: dictionaries instead of lists

# No header comments for the functions anymore, as each function does the same thing, at a high level, as it did in the last version.

def one(gen):
    return next(gen, None)

# A helper function that causes a dictionary lookup to return None instead of raising an exception
def get(dict, key):
    if key in dict:
        return dict[key]
    else:
        return None

# And a helpful version for traversing nested dictionaries
def get2(dict1, key1, key2):
    dict2 = get(dict1, key1)
    if dict2:
        return get(dict2, key2)
    else:
        return None

def empty():
    return {"students": {},
            "psets": {},
            "grades": {}}
# There's a good chance you can guess how "students" and "psets" work as dictionaries.
# It's natural to use each kind of ID as a key.
# Grades are less obvious.  There are at least three reasonable dictionary choices:
#  [Student ID] |-> [Pset ID] |-> [Points]
#  [Pset ID] |-> [Student ID] |-> [Points]
#  [(Student ID, Pset ID)] |-> [Points]
# We're going to use the first one, which is optimized for fast lookup of grades by
# students.

def addStudent(db, student_id, student_name):
    db["students"][student_id] = student_name

def studentIdFromName(db, student_name):
    return one(id
               for id, name in db["students"].items()
               if name == student_name)

def studentNameFromId(db, student_id):
    return get(db["students"], student_id)

def addPset(db, pset_id, pset_total_points):
    db["psets"][pset_id] = pset_total_points

def psetPointsFromId(db, pset_id):
    return get(db["psets"], pset_id)

def addGrade(db, student_id, pset_id, points):
    if student_id not in db["grades"]:
        db["grades"][student_id] = {}

    db["grades"][student_id][pset_id] = points

def gradeOn(db, student_id, pset_id):
    return get2(db["grades"], student_id, pset_id)

# Our representation of grades really shines here!
def studentGrades(db, student_id):
    return get(db["grades"], student_id)

def gradesOnPset(db, pset_id):
    return {db["students"][student]: psets[pset_id]
            for student, psets in db["grades"].items()
            if pset_id in psets}

def gradeOnWeighted(db, student_id, pset_id, pset_points):
    grade = gradeOn(db, student_id, pset_id)
    if grade == None:
        return 0
    else:
        return grade * 1.0 / pset_points
def studentGradesWeighted(db, student_id):
    return [gradeOnWeighted(db, student_id, pset_id, pset_points)
            for pset_id, pset_points in db["psets"].items()]

def finalGradeOf(db, student_id):
    grades = studentGradesWeighted(db, student_id)
    return round(sum(grades) / len(grades) * 100, 1)

def finalGrades(db):
    return [{"id": id,
             "name": name,
             "grade": finalGradeOf(db, id)}
            for id, name in db["students"].items()]

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

print (db["grades"])

print (finalGrades(db))
