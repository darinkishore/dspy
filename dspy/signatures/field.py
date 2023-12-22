import re
import dsp

class Field:
    """A more ergonomic datatype that infers prefix and desc if omitted."""
    def __init__(self, *, prefix=None, desc=None, input, format=None):
        """Initializes the Field instance with the given parameters.

        :param prefix: Optional prefix for the field. If not provided, it will be inferred.
        :param desc: Optional description for the field. If not provided, it will be inferred.
        :param input: Specifies if the field is for input. Otherwise, it's for output.
        :param format: The format of the field, if applicable.
        """
        self.prefix = prefix  # This can be None initially and set later
        self.desc = desc
        self.format = format
        
    def finalize(self, key, inferred_prefix):
        """Sets the prefix for the field if it's not provided explicitly and updates the description.

        :param key: The key identifying the field in the signature.
        :param inferred_prefix: The prefix inferred for the field.
        :return: None
        """
        """Set the prefix if it's not provided explicitly."""
        if self.prefix is None:
            self.prefix = inferred_prefix + ":"
        
        if self.desc is None:
            self.desc = f'${{{key}}}'
        
    def __repr__(self):
        """Represents the Field instance as a string.

        :return: The string representation of the Field instance.
        """
        return f"{self.__class__.__name__}(prefix={self.prefix}, desc={self.desc})"
    
    def __eq__(self, __value: object) -> bool:
        """Determines if this Field instance is equal to another object.

        :param __value: The object to compare against.
        :return: True if objects are equal, False otherwise.
        """
        return self.__dict__ == __value.__dict__

class InputField(Field):
    """A subclass of Field that specifically represents input fields, inheriting the functionality and allowing further specification.
    """
    def __init__(self, *, prefix=None, desc=None, format=None):
        super().__init__(prefix=prefix, desc=desc, input=True, format=format)

class OutputField(Field):
    """A subclass of Field that specifically represents output fields, inheriting the functionality and allowing further specification.
    """
    def __init__(self, *, prefix=None, desc=None, format=None):
        super().__init__(prefix=prefix, desc=desc, input=False, format=format)
