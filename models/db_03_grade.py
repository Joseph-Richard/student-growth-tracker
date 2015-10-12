# -*- coding: utf-8 -*-
db.define_table(
    'grade',
    Field('name', required=True, requires=IS_NOT_EMPTY()),
    Field('sequenceDate', 'integer', requires=IS_NOT_EMPTY()),
    Field('passFail', 'boolean', requires=IS_NOT_EMPTY()),
    Field('keywords'),
    Field('dueDate', 'integer', requires=IS_NOT_EMPTY()),
    format = '%(name)s')
db.class_.id.readable = db.class_.id.writable = False