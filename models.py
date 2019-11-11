from meta_model import Model
from fields.simple_fields import FieldInt, FieldStr, OneToManyField


class User(Model):
    __table__ = 'user'

    id: FieldInt = FieldInt(pk = True)
    name: FieldStr = FieldStr()
    age: FieldInt = FieldInt()

    address: OneToManyField = OneToManyField(related_model='Address', from_link='id', to_link='user_id')
    question: OneToManyField = OneToManyField(related_model='Question', from_link='id', to_link='id')


class Address(Model):
    __table__ = 'address'

    id: FieldInt = FieldInt(pk = True)
    descr: FieldStr = FieldStr()
    user_id: FieldInt = FieldInt()

class Question(Model):
    __table__ = 'question'

    id: FieldInt = FieldInt(pk = True)
    descr: FieldStr = FieldStr()