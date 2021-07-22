
## Version #3: redundant dictionaries to support fast implementations of more operations

def one(gen):
    return next(gen, None)

def get(dict, key):
    if key in dict:
        return dict[key]
    else:
        return None

def get2(dict1, key1, key2):
    dict2 = get(dict1, key1)
    if dict2:
        return get(dict2, key2)
    else:
        return None

# Here's a helper function that embodies a code pattern we used in the last version,

# to add to a nested dictionary.
def add2(dict1, key1, key2, value):
    if key1 not in dict1:
        dict1[key1] = {}

    dict1[key1][key2] = value
def empty():
    return {"studentsById": {},
            "studentsByName": {},
            "psets": {},
            "gradesByStudent": {},
            "gradesByPset": {}}

def addStudent(db, student_id, student_name):
    db["studentsById"][student_id] = student_name
    db["studentsByName"][student_name] = student_id

def studentIdFromName(db, student_name):
    return get(db["studentsByName"], student_name)

def studentNameFromId(db, student_id):
    return get(db["studentsById"], student_id)

def addPset(db, pset_id, pset_total_points):
    db["psets"][pset_id] = pset_total_points

def psetPointsFromId(db, pset_id):
    return get(db["psets"], pset_id)

def addGrade(db, student_id, pset_id, points):
    add2(db["gradesByStudent"], student_id, pset_id, points)
    add2(db["gradesByPset"], pset_id, student_id, points)

def gradeOn(db, student_id, pset_id):
    return get2(db["gradesByStudent"], student_id, pset_id)

def studentGrades(db, student_id):
    return get(db["gradesByStudent"], student_id)

def gradesOnPset(db, pset_id):
    students = get(db["gradesByPset"], pset_id)
    if students:
        return {db["studentsById"][student_id]: points
            for student_id, points in students.items()}
    else:
        return {}

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
            for id, name in db["studentsById"].items()]

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

print (finalGrades(db))
