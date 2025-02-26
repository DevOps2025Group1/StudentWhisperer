from typing import List, Dict

class Student:
    def __init__(self, student_id: int, name: str, email: str, courses: List[Dict[str, str]]):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.courses = courses

    def __repr__(self) -> str:
        return f"Student(id={self.student_id}, name={self.name}, email={self.email}, courses={self.courses})"
