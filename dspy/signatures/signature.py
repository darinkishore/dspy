import re
import dsp

from .field import Field, InputField, OutputField
import threading

class SignatureMeta(type):
    """A metaclass for the Signature class in the DSPy framework."""
    _thread_local_storage = threading.local()

    class _SignatureNamespace:
        def __init__(self, fields):
            for key, value in fields.items():
                setattr(self, key, value)

        def input_fields(self):
            return {k: v for k, v in self.__dict__.items() if isinstance(v, InputField)}

        def output_fields(self):
            return {k: v for k, v in self.__dict__.items() if isinstance(v, OutputField)}
    

    def __new__(cls, name, bases, class_dict):
        type_attributes = {}

        for k, v in list(class_dict.items()):
            if isinstance(v, Field):
                v.finalize(k, infer_prefix(k))
                type_attributes[k] = v
                del class_dict[k]

        instructions = class_dict.get('__doc__') or ""

        new_class = super().__new__(cls, name, bases, class_dict)

        # Attach the _SignatureNamespace directly to the class
        setattr(new_class, 'signature', cls._SignatureNamespace(type_attributes))

        # Create and attach the template directly to the class
        setattr(new_class, '_template', dsp.Template(instructions=instructions, **type_attributes))

        return new_class

    @property
    def kwargs(cls):
        return cls.signature.fields
    
    def __call__(cls, *args, **kwargs):
        """Calls a Signature instance or creates a new one based on the provided arguments.

        :param args: Positional arguments for the function call.
        :param kwargs: Keyword arguments for the function call.
        :return: A Signature instance or the result from the `_template` call.
        """
        if len(args) == 1 and isinstance(args[0], str):
            instance = super(SignatureMeta, cls).__call__(*args, **kwargs)
            return instance
        #old 
        return cls._template(*args, **kwargs)

    def __getattr__(cls, attr):
        """Gets the attribute from the _template object if not found in the class's dictionary.

        :param attr: The name of the attribute to get.
        :return: The value of the attribute from the _template object.
        """
        # Redirect attribute access to the template object when accessed on the class directly
        if attr not in cls.__dict__:
            return getattr(cls._template, attr)
        return super().__getattr__(attr)    

class Signature(metaclass=SignatureMeta):
    """Class used to declare the input/output behavior of LMs in DSPy.

    A Signature instance encapsulates descriptions for input and output fields
    of a sub-task, allowing DSPy modules to interact with large LMs efficiently.
    """
    def __init__(self, signature: str = "", instructions: str = ""):
        """Initializes the Signature instance with a signature string and instructions.

        :param signature: A string defining the input and output fields.
        :param instructions: Additional instructions for the signature.
        """
        self.signature = signature
        self.instructions = instructions
        self.fields = {}
        self.parse_structure()
    
    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return getattr(self.__class__, attr)
        return super().__getattr__(attr)

    @property
    def kwargs(self):
        return {k: v for k, v in self.fields.items()}

    def parse_structure(self):
        """Parses the signature string to extract and define input and output fields.

        :return: None
        """
        inputs_str, outputs_str = self.signature.split("->")
        for name in inputs_str.split(","):
            self.add_field(name.strip(), InputField())
        for name in outputs_str.split(","):
            self.add_field(name.strip(), OutputField())

    def attach(self, **kwargs):
        """Attaches fields to the Signature with additional properties like prefix and description.

        :param kwargs: A dictionary with field names as keys and tuples of (prefix, desc) as values.
        :return: The instance of Signature for chaining method calls.
        """
        for key, (prefix, desc) in kwargs.items():
            field_type = self.fields.get(key)
            if not field_type:
                raise ValueError(f"{key} does not exist in this signature")
            field_map = {
                InputField: InputField(prefix=prefix, desc=desc),
                OutputField: OutputField(prefix=prefix, desc=desc)
            }
            self.fields[key] = field_map.get(type(field_type))
        return self

    def add_field(self, field_name: str, field_type, position="append"):
        """Adds a field to the Signature with the specified field name and type.

        :param field_name: The name of the field to add.
        :param field_type: The type of field being added, can be InputField or OutputField.
        :param position: Specifies whether to append or prepend the new field in the fields order.
        :return: None
        """
        if field_name in self.fields:
            raise ValueError(f"{field_name} already exists in fields.")
        if isinstance(field_type, (InputField, OutputField)):
            field_instance = field_type
        else:
            raise ValueError(f"non-existent {field_type}.")
        if isinstance(field_instance, InputField) and position == "append":
            input_fields = self.input_fields()
            if input_fields:
                last_input_key = list(input_fields.keys())[-1]
                index = list(self.fields.keys()).index(last_input_key) + 1
                self.fields = {**dict(list(self.fields.items())[:index]), field_name: field_instance, **dict(list(self.fields.items())[index:])}
            else:
                self.fields[field_name] = field_instance
        elif isinstance(field_instance, OutputField) and position == "prepend":
            output_fields = self.output_fields()
            if output_fields:
                first_output_key = list(output_fields.keys())[0]
                index = list(self.fields.keys()).index(first_output_key)
                self.fields = {**dict(list(self.fields.items())[:index]), field_name: field_instance, **dict(list(self.fields.items())[index:])}
            else:
                self.fields[field_name] = field_instance
        elif position == "prepend":
            self.fields = {field_name: field_instance, **self.fields}
        elif position == "append":
            self.fields[field_name] = field_instance
        else:
            raise ValueError(f"invalid field addition. Please verify that your field name: {field_name}, field_type: {field_type}, and expected position: {position} are correct.")

    def input_fields(self):
        return {k: v for k, v in self.fields.items() if isinstance(v, InputField)}

    def output_fields(self):
        return {k: v for k, v in self.fields.items() if isinstance(v, OutputField)}

    def __repr__(self):
        s = []
        for name, _ in self.fields.items():
            value = getattr(self, name, None)
            if value:
                s.append(f"- {name} = {value}")
            else:
                s.append(f"- {name} = [field not attached]")
        return f'{self.__class__.__name__}\n' + '\n'.join(s)

    def __eq__(self, __value: object) -> bool:
        return self._template == __value._template



def infer_prefix(attribute_name: str) -> str:
    """Infers a prefix from an attribute name."""
    
    # Convert camelCase to snake_case, but handle sequences of capital letters properly
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attribute_name)
    intermediate_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)

    # Insert underscores around numbers to ensure spaces in the final output
    with_underscores_around_numbers = re.sub('([a-zA-Z])(\d)', r'\1_\2', intermediate_name)
    with_underscores_around_numbers = re.sub('(\d)([a-zA-Z])', r'\1_\2', with_underscores_around_numbers)

    # Convert snake_case to 'Proper Title Case', but ensure acronyms are uppercased
    words = with_underscores_around_numbers.split('_')
    title_cased_words = []
    for word in words:
        if word.isupper():
            title_cased_words.append(word)
        else:
            title_cased_words.append(word.capitalize())
    
    return ' '.join(title_cased_words)

### Testing the function
assert infer_prefix('someAttributeName42IsCool') == 'Some Attribute Name 42 Is Cool'
assert infer_prefix('version2Update') == 'Version 2 Update'
assert infer_prefix('modelT45Enhanced') == 'Model T 45 Enhanced'
assert infer_prefix('someAttributeName') == 'Some Attribute Name'
assert infer_prefix('some_attribute_name') == 'Some Attribute Name'
assert infer_prefix('URLAddress') == 'URL Address'
assert infer_prefix('isHTTPSecure') == 'Is HTTP Secure'
assert infer_prefix('isHTTPSSecure123') == 'Is HTTPS Secure 123'