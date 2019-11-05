import typing

ConnGen = typing.TypeVar('ConnGen')

def get_all_property(annot, cls_dict):
    for i in cls_dict:
        if i in annot:
            yield i