from dataclasses import fields, is_dataclass
from typing import Type, TypeVar, Dict

T = TypeVar("T")


class JSONutils:
    '''
    An util class to handle stuff related to JSON.'''


    @staticmethod
    def JSON2Class(json_dict: Dict, cls: Type[T]) -> T:
        '''
        Convert a JSON to a class object based on the fields present.
        Only the common fileds are set. The rest are ignored.
        Args:
            jsonDict (dict): The JSON to be converted.
            classObj (object): The class object to be set.
        '''

        if not is_dataclass(cls):
            raise ValueError(f"{cls} is not a dataclass")
        
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in json_dict.items() if k in field_names}
        return cls(**filtered_data)

    