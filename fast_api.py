from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from typing import Dict, Optional

app = FastAPI(title="Classroom Marks API")

# --- In-Memory Database ---
# Format: { student_id: { "name": str, "math": int, "science": int, "english": int } }
marks_db: Dict[int, dict] = {
    101: {"name": "Aarav", "math": 88, "science": 92, "english": 85},
    102: {"name": "Diya", "math": 76, "science": 81, "english": 79},
}

# --- Pydantic Schemas ---
class StudentCreate(BaseModel):
    name: str
    math: int = Field(ge=0, le=100)
    science: int = Field(ge=0, le=100)
    english: int = Field(ge=0, le=100)

class StudentUpdateFull(BaseModel):
    name: str
    math: int = Field(ge=0, le=100)
    science: int = Field(ge=0, le=100)
    english: int = Field(ge=0, le=100)

class StudentUpdatePartial(BaseModel):
    name: Optional[str] = None
    math: Optional[int] = Field(default=None, ge=0, le=100)
    science: Optional[int] = Field(default=None, ge=0, le=100)
    english: Optional[int] = Field(default=None, ge=0, le=100)


# 1. GET - Retrieve all student marks or a specific student's record
@app.get("/students", status_code=status.HTTP_200_OK)
def get_all_marks():
    return marks_db

@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
def get_student_marks(student_id: int):
    if student_id not in marks_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student_id": student_id, "data": marks_db[student_id]}


# 2. POST - Create a new student record
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student_record(student: StudentCreate):
    new_id = max(marks_db.keys(), default=100) + 1
    marks_db[new_id] = student.model_dump()
    return {"message": "Record created", "student_id": new_id, "data": marks_db[new_id]}


# 3. PUT - Full replacement/overwrite of an existing student record
@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
def replace_student_record(student_id: int, student: StudentUpdateFull):
    if student_id not in marks_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Overwrites entire record
    marks_db[student_id] = student.model_dump()
    return {"message": "Record fully updated", "data": marks_db[student_id]}


# 4. PATCH - Partially update specific fields (e.g., updating only Math marks)
@app.patch("/students/{student_id}", status_code=status.HTTP_200_OK)
def update_partial_marks(student_id: int, updates: StudentUpdatePartial):
    if student_id not in marks_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    current_data = marks_db[student_id]
    # Extract only fields explicitly passed in the request body
    update_data = updates.model_dump(exclude_unset=True)
    
    current_data.update(update_data)
    marks_db[student_id] = current_data
    return {"message": "Record partially updated", "data": marks_db[student_id]}


# 5. DELETE - Remove a student record
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_record(student_id: int):
    if student_id not in marks_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del marks_db[student_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 6. HEAD - Returns headers only (e.g., check existence or cached size) without body
@app.head("/students/{student_id}")
def check_student_record_headers(student_id: int, response: Response):
    if student_id not in marks_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Custom headers convey metadata; no response body is returned
    response.headers["X-Record-Exists"] = "true"
    response.headers["X-Subject-Count"] = "3"
    return Response(status_code=status.HTTP_200_OK, headers=response.headers)


# 7. OPTIONS - Informs clients which HTTP methods are supported for this resource
@app.options("/students/{student_id}")
def options_student_resource(response: Response):
    response.headers["Allow"] = "GET, PUT, PATCH, DELETE, HEAD, OPTIONS"
    return Response(status_code=status.HTTP_200_OK, headers=response.headers)