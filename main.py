from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    2: {"name": "John",
        "age": 20,
        "birth_month": "June"}
}


class Student(BaseModel):
    name: str
    age: int
    birth_month: str


class Update(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    birth_month: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/student/{id_student}")
def student_id(id_student: int = Path(None, description="ENTER STUDENT ID TO VIEW DETAILS", gt=1)):
    return students[id_student]


@app.get("/student-name")
def students_name(*, id_student, name: Optional[str] = None):
    for id_student in students:
        if students[id_student]["name"] == name:
            return students[id_student]
    return {"message": "Student not found"}


@app.post("/create-student/{id_student}")
def create_student(id_student: int, student: Student):
    if id_student in students:
        return {"Error": "Student exist"}

    students[id_student] = student
    return students[id_student]


@app.put("/update-student/{id_student}")
def update_student(id_student: int, update: Update):
    if id_student not in students:
        return {"MessageError": "Student does not exist"}

    if update.name != None:
        students[id_student].name = update.name

    if update.age != None:
        students[id_student].age = update.age

    if update.birth_month != None:
        students[id_student].birth_month = update.birth_month

    return students[id_student]


@app.delete("/delete-student/{id_student}")
def delete_student(id_student: int):
    if id_student not in students:
        return {"ErrorSearching": "student does not exist"}
    del students[id_student]
    return {"Message": "Student deleted successfully"}
