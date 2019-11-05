from .meta_field import MetaField

class FieldStr(MetaField):
    def __str__(self,) -> str:
        return str(self.value)


class FieldInt(MetaField):
    def __str__(self,) -> str:
        return str(self.value)