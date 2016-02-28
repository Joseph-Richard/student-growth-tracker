# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from notifications.py")

@auth.requires_login()
def detect_trends():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    students_query = (db.student.id> 0)
    students = db(students_query).select(db.student.id)
    student_count = 0
    class_count = 0
    assignment_count = 0
    assignment_list = []
    student_average_values_list = []
    for student in students:
        student_count += 1
        class_query = ((db.student_classes.student_id == student.id)&
                       (db.student_classes.class_id == db.classes.id))
        classes = db(class_query).select(db.classes.id)
        count_i = 0
        count_j = 0
        count_k = 0
        assignment_dict = {}
        for single_class in classes:
            class_count += 1
            assignments = assignments = get_student_assignment_list(student.id, single_class.id)
            student_score= 0
            student_possible = 0
            student_missing_assignments = 0
            for assignment in assignments:
                assignment_count += 1
                student_score += assignment.student_grade.student_score
                student_possible += assignment.grade.score
                grade_info = [assignment.grade.name, assignment.student_grade.student_score, assignment.grade.score]
                assignment_list.append(grade_info)
                if (student_score == 0):
                    student_missing_assignments += 1
            average_values = [student.id, single_class.id, student_score, student_possible]
            student_average_values_list.append(average_values)
            student_average = student_score/student_possible
            if (student_average < .75):
                db.notifications.insert(student_id=student.id,
                                        class_id=single_class.id,
                                        date=datetime.datetime.now,
                                        warning_text=("Student Grade is less than 75%."))
            if (student_missing_assignments > 5):
                db.notifications.insert(student_id=student.id,
                                        class_id=single_class.id,
                                        date=datetime.datetime.now,
                                        warning_text=("Student is missing excessive grades."))
    session.flash="Trend Database Populated with New Warnings."
    #returns are largely still for testing purposes
#    return dict(student_count=student_count,
#                 class_count=class_count,
#                 assignment_count=assignment_count,
#                 assignment_dict=assignment_dict,
#                 assignment_list=assignment_list,
#                 student_average_values_list=student_average_values_list
#                 )
    return dict(redirect(URL('admin','index')))
