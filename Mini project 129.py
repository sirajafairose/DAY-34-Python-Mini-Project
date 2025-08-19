#School Report Card Generator


class Person:
    def __init__(self, name, age):
        self._name = name         
        self._age = age

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def __str__(self):
        return f"{self._name}, Age: {self._age}"



class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self._student_id = student_id
        self._subjects = {}   

    def enroll_subject(self, subject):
        self._subjects[subject.name] = 0

    def update_marks(self, subject_name, marks):
        if subject_name in self._subjects:
            self._subjects[subject_name] = marks

    def get_marks(self, subject_name):
        return self._subjects.get(subject_name, None)

    def get_all_subjects(self):
        return self._subjects

    def __str__(self):
        return f"Student: {self.get_name()} (ID: {self._student_id})"

    @classmethod
    def from_dict(cls, data):
        """Create student from dictionary (example of classmethod)."""
        return cls(data["name"], data["age"], data["student_id"])



class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def assign_marks(self, student, marks):
        student.update_marks(self.subject.name, marks)

    def __str__(self):
        return f"Teacher: {self.get_name()} | Subject: {self.subject.name}"


\
class Subject:
    def __init__(self, name, max_marks=100, grading_system="percentage"):
        self.name = name
        self.max_marks = max_marks
        self.grading_system = grading_system

    def grade(self, marks):
        """Polymorphism: Different grading logic based on system."""
        if self.grading_system == "percentage":
            percentage = (marks / self.max_marks) * 100
            if percentage >= 90: return "A"
            elif percentage >= 75: return "B"
            elif percentage >= 50: return "C"
            else: return "F"

        elif self.grading_system == "gpa":
            gpa = (marks / self.max_marks) * 4
            return round(gpa, 2)

        elif self.grading_system == "passfail":
            return "Pass" if marks >= (self.max_marks * 0.4) else "Fail"

        else:
            return "Invalid grading system"

    def __str__(self):
        return f"Subject: {self.name} | System: {self.grading_system}"



class ReportCard:
    def __init__(self, student):
        self.student = student

    def generate(self, subjects):
        print(f"\n📘 Report Card for {self.student.get_name()}")
        print("-" * 40)
        for subject in subjects:
            marks = self.student.get_marks(subject.name)
            if marks is not None:
                grade = subject.grade(marks)  # Polymorphism in action
                print(f"{subject.name:<15} Marks: {marks:<5} Grade: {grade}")
            else:
                print(f"{subject.name:<15} Not Enrolled")
        print("-" * 40)



if __name__ == "__main__":

    math = Subject("Mathematics", 100, "percentage")
    physics = Subject("Physics", 100, "gpa")
    sports = Subject("Sports", 50, "passfail")

 
    s1 = Student("Alice", 15, "S001")
    s1.enroll_subject(math)
    s1.enroll_subject(physics)
    s1.enroll_subject(sports)

 
    t1 = Teacher("Mr. Smith", 40, math)
    t2 = Teacher("Dr. Brown", 45, physics)
    t3 = Teacher("Coach Lee", 35, sports)

    t1.assign_marks(s1, 88)
    t2.assign_marks(s1, 76)
    t3.assign_marks(s1, 20)


    rc = ReportCard(s1)
    rc.generate([math, physics, sports])
