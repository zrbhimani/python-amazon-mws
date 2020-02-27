from collections.abc import Mapping

def _snake_case_to_camelcase(a_str):
    """
    Converts a snack_case_string into its CamelCaseEquivalent.
    """
    return ''.join(
        [x.title() for x in a_str.split('_')]
    )

class BaseDataType(Mapping):
    """
    Base functionality shared across Datatype classes.
    """
    __slots__ = ()
    """Define the attributes of the subclassing Datatype as a string entry in __slots__,
    otherwise you won't be able to add the attribute in later.
    """
    def parameterized(self, prefix=""):
        output = {}
        if not prefix:
            prefix = ""
        elif not prefix.endswith("."):
            prefix += "."
        for key, val in self.items():
            if val is None:
                continue
            camel_key = _snake_case_to_camelcase(key)
            new_key = "{}{}".format(prefix, camel_key)
            if isinstance(val, BaseDataType):
                output.update(val.parameterized(prefix=new_key))
            else:
                output[new_key] = val
        return output

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __len__(self):
        return len(self.__slots__)

    def __iter__(self):
        return iter(self.__slots__)

    def items(self):
        for attribute in self.__slots__:
            yield attribute, getattr(self, attribute)
