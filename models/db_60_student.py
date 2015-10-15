#Student table creation
db.define_table(
    'student',
    Field('user_id', 'reference auth_user'),
    Field('school_id_number','string', requires=IS_NOT_EMPTY),
    Field('grade_level','integer', requires=IS_NOT_EMPTY),
    format = '%(ID)s')
db.classes.id.readable = db.classes.id.writable = False

db.define_table(
    'student_classes',
    Field('student_id', 'reference student'),
    Field('class_id', 'reference classes'))
db.student_classes.student_id.readable = db.student_classes.student_id.writable = False
db.student_classes.class_id.readable = db.student_classes.class_id.writable = False
