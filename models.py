from meta_model import Model
from fields.simple_fields import FieldInt, FieldStr, OneToOneField


class User(Model):
    __table__ = 'user'

    id: FieldInt = FieldInt(pk = True)
    name: FieldStr = FieldStr()
    age: FieldInt = FieldInt()

    address: OneToOneField = OneToOneField(related_model='Address', from_link='id', to_link='id')
    question: OneToOneField = OneToOneField(related_model='Question', from_link='id', to_link='id')


class Address(Model):
    __table__ = 'address'

    id: FieldInt = FieldInt(pk = True)
    descr: FieldStr = FieldStr()

class Question(Model):
    __table__ = 'question'

    id: FieldInt = FieldInt(pk = True)
    descr: FieldStr = FieldStr()