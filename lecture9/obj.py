

## Version #4: now all dictionaries for a particular sort of
## entity map to the same underlying _objects_.

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
    student = {"id": student_id,
               "name": student_name}

    db["studentsById"][student_id] = student
    db["studentsByName"][student_name] = student

def studentId(student):
    return get(student, "id")
def studentName(student):
    return get(student, "name")

def studentFromName(db, student_name):
    return get(db["studentsByName"], student_name)

def studentIdFromName(db, student_name):
    return studentId(studentFromName(db, student_name))

def studentFromId(db, student_id):
    return get(db["studentsById"], student_id)

def studentNameFromId(db, student_id):
    return studentName(studentFromId(db, student_id))

def addPset(db, pset_id, pset_total_points):
    pset = {"id": pset_id,
            "points": pset_total_points}

    db["psets"][pset_id] = pset

def psetPoints(pset):
    return get(pset, "points")

def psetFromId(db, pset_id):
    return get(db["psets"], pset_id)

def psetPointsFromId(db, pset_id):
    return psetPoints(psetFromId(db, pset_id))

def addGrade(db, student_id, pset_id, points):
    grade = {"student": student_id,
             "pset": pset_id,
             "points": points}

    add2(db["gradesByStudent"], student_id, pset_id, grade)
    add2(db["gradesByPset"], pset_id, student_id, grade)

def gradeOn(db, student_id, pset_id):
    return get3(db["gradesByStudent"], student_id, pset_id, "points")

def studentGrades(db, student_id):
    return {grade["pset"]: grade["points"]
            for grade in get(db["gradesByStudent"], student_id).values()}

def gradesOnPset(db, pset_id):
    students = get(db["gradesByPset"], pset_id)
    if students:
        return {db["studentsById"][student_id]["name"]: grade["points"]
            for student_id, grade in students.items()}
    else:
        return {}

def gradeOnWeighted(db, student_id, pset_id, pset_points):
    grade = gradeOn(db, student_id, pset_id)
    if grade == None:
        return 0
    else:
        return grade * 1.0 / pset_points
def studentGradesWeighted(db, student_id):
    return [gradeOnWeighted(db, student_id, pset["id"], pset["points"])
            for pset in db["psets"].values()]

def finalGradeOf(db, student_id):
    grades = studentGradesWeighted(db, student_id)
    return round(sum(grades) / len(grades) * 100, 1)

def finalGrades(db):
    return [{"id": student["id"],
             "name": student["name"],
             "grade": finalGradeOf(db, student["id"])}
            for student in db["studentsById"].values()]


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
