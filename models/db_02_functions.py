"""
db_02_functions.py
==================

This module contains functions that generate queries or return data sets
to be used in the **Student Growth Tracker** application.

Functions that return a :py:class:`Query <pydal.objects.Query>` object
have names that end with ``_query``.

Functions that return sets of values have names that start with ``get_``.
"""

def teacher_classes_query(teacher_id, class_id=None):
    """
    Return a :py:class:`Query <pydal.objects.Query>` object that represents the
    set of classes associated with ``teacher_id``. If ``class_id`` is provided,
    only that class will be included in the :py:class:`Set <pydal.objects.Set>`.
    """
    query = ((db.gradebook.teacher==teacher_id) &
             (db.gradebook.classes==db.classes.id) &
             (db.classes.content_area==db.contentarea.id))

    if class_id:
        query &= (db.gradebook.classes==class_id)

    return query

def get_class_list(teacher_id):
    """
    Return a :py:class:`Rows <pydal.objects.Rows>` object containing the classes
    associated with the teacher.

    Each :py:class:`Row <pydal.objects.Row>` object has the following fields:

    - ``classes.id``
    - ``classes.name``
    - ``contentarea.id``
    - ``contentarea.name``
    """
    query = teacher_classes_query(teacher_id)
    result = db(query).select(db.classes.id, db.classes.name, db.contentarea.id,
                              db.contentarea.name)
    return result

def get_class_roster(teacher_id, class_id):
    """
    Return a :py:class:`list` of lists of students in the class
    with id ``class_id``. Each list item is a two-element list
    with the format::

        [student.id, auth_user.first_name + ' ' + auth_user.last_name]
    """
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.id==db.student_classes.class_id) &
             (db.student_classes.student_id==db.student.id) &
             (db.student.user_id==db.auth_user.id))
    results = db(query).select(db.student.id,
                               db.auth_user.first_name,
                               db.auth_user.last_name)

    class_roster = []
    for s in results:
        class_roster.append([int(s.student.id),
                             s.auth_user.first_name + ' ' + s.auth_user.last_name])

    return class_roster

def get_class_assignments(teacher_id, class_id):
    """
    Return a :py:class:`Rows <pydal.objects.Rows>` object containing
    all of the assignments for the class with id ``class_id``, sorted
    by due date.

    Each :py:class:`Row <pydal.objects.Row>` object has the following fields:

    - ``grade.name``
    """
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.id==db.class_grade.class_id) &
             (db.class_grade.grade_id==db.grade.id))

    class_assignments = db(query).select(db.grade.name,
                                         orderby=db.grade.due_date)

    return class_assignments

def get_student_assignments(teacher_id, class_id):
    """
    Returns a :py:class:`list` of lists containing the student grades
    for all assignments for the class with id ``class_id``.

    The output of this function is formatted to be used as the
    data source for a Handsontable object. The first row of the
    list contains the names of the assignments. The remainder of
    the rows contain the assignment grades for each student.

    The *rows* are ordered by student id, and the columns are
    ordered by due date.
    """
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.id==db.student_classes.class_id) &
             (db.student_classes.student_id==db.student.id) &
             (db.student.user_id==db.auth_user.id) &
             (db.student.id==db.student_grade.student_id) &
             (db.student_grade.grade_id==db.grade.id))

    results = db(query).select(db.student.id,
                               db.auth_user.first_name,
                               db.auth_user.last_name,
                               db.grade.name,
                               db.student_grade.student_score,
                               db.student_grade.id,
                               orderby=[db.student.id,
                                        db.grade.due_date])

    anames = ['', '']
    for a in get_class_assignments(teacher_id, class_id):
        anames.append(a.name)

    assignments = [anames]

    for student in get_class_roster(teacher_id, class_id):
        grades = results.find(lambda s: s.student.id==student[0])
        for grade in grades:
            student.append(grade.student_grade.student_score)
        assignments.append(student)

    return assignments

if __name__ == '__main__':
    pass
