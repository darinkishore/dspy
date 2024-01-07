import copy

class Example:
    """
    The Example class is a flexible container for storing and manipulating key-value pairs.
    It provides methods for accessing, setting, and deleting items, as well as other utility methods.
    """
    def __init__(self, base=None, **kwargs):
        """
        Initialize a new instance of the Example class.

        Args:
            base (Example or dict, optional): If an Example instance is provided, its internal storage is copied.
                If a dict is provided, it is copied. Defaults to None.
            **kwargs: Additional key-value pairs to add to the internal storage.
        """
        """
        # Internal storage and other attributes
        self._store = {}
        self._demos = []
        self._input_keys = None

        # Initialize from a base Example if provided
        if base and isinstance(base, type(self)):
            self._store = base._store.copy()

        # Initialize from a dict if provided
        elif base and isinstance(base, dict):
            self._store = base.copy()

        # Update with provided kwargs
        self._store.update(kwargs)
    
    def __getattr__(self, key):
        """
        Attempt to access the value of an instance attribute that is not part of the standard properties of the object but is expected to be in the _store dictionary.

        Args:
            key (str): The name of the attribute.

        Raises:
            AttributeError: If the attribute does not exist.

        Returns:
            Any: The value of the attribute.
        """
        if key.startswith('__') and key.endswith('__'):
            raise AttributeError
        if key in self._store:
            return self._store[key]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        """
        Set a new attribute of the object. If the key doesn't start with an underscore and isn't a built-in property/method name, the (key, value) pair is stored in the _store dictionary instead of setting an object attribute.

        Args:
            key (str): The name of the attribute.
            value (Any): The value to set the attribute to.
        """
        if key.startswith('_') or key in dir(self.__class__):  
            super().__setattr__(key, value)
        else:
            self._store[key] = value
    
    def __getitem__(self, key):
        """
        Get an item from the Example instance using key indexing.

        Args:
            key (str): The key of the item.

        Returns:
            Any: The value of the item.
        """
        return self._store[key]

    def __setitem__(self, key, value):
        """
        Set an item of the Example instance using key indexing.

        Args:
            key (str): The key of the item.
            value (Any): The value to set the item to.
        """
        """
        Add or update an item in the Example instance's internal store using dictionary-style key assignment.
        """
        self._store[key] = value

    def __delitem__(self, key):
        """
        Delete an item from the Example instance using key indexing.

        Args:
            key (str): The key of the item.
        """
        del self._store[key]

    def __contains__(self, key):
        """
        Check if an item exists in the Example instance.

        Args:
            key (str): The key of the item.

        Returns:
            bool: True if the item exists, False otherwise.
        """
        return key in self._store
    
    def __len__(self):
        return len([k for k in self._store if not k.startswith('dspy_')])
    
    def __repr__(self):
        """
        Provide a string representation of the Example instance excluding private properties prefixed with 'dspy_'.
        """
        # return f"Example({self._store})" + f" (input_keys={self._input_keys}, demos={self._demos})"
        d = {k: v for k, v in self._store.items() if not k.startswith('dspy_')}
        return f"Example({d})" + f" (input_keys={self._input_keys})"
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        return self._store == other._store
    
    def __hash__(self):
        return hash(tuple(self._store.items()))

    def keys(self, include_dspy=False):
        return [k for k in self._store.keys() if not k.startswith('dspy_') or include_dspy]
    
    def values(self, include_dspy=False):
        return [v for k, v in self._store.items() if not k.startswith('dspy_') or include_dspy]

    def items(self, include_dspy=False):
        return [(k, v) for k, v in self._store.items() if not k.startswith('dspy_') or include_dspy]

    def get(self, key, default=None):
        """
        Retrieve the value associated with the given key from the instance's store, or return the default if the key is not found.

        Args:
            key (str): The key to retrieve the value for.
            default (any, optional): The value to return if the key is not found. Default is None.

        Returns:
            The value associated with the key, or the default value.
        """
        return self._store.get(key, default)
    
    def with_inputs(self, *keys):
        copied = self.copy()
        copied._input_keys = set(keys)
        return copied
    
    def inputs(self):
        if self._input_keys is None:
            raise ValueError("Inputs have not been set for this example. Use `example.with_inputs()` to set them.")

        # return items that are in input_keys
        """
        Retrieve a new Example instance containing only the key-value pairs where the keys are specified as inputs.

        Raises:
            ValueError: If the input keys have not been set prior to invocation of this method.

        Returns:
            Example: A new Example instance containing only key-value pairs specified as inputs.
        """
        d = {key: self._store[key] for key in self._store if key in self._input_keys}
        return type(self)(d)
    
    def labels(self):
        # return items that are NOT in input_keys
        input_keys = self.inputs().keys()
        d = {key: self._store[key] for key in self._store if key not in input_keys}
        return type(self)(d)
    
    def __iter__(self):
        return iter(dict(self._store))

    def copy(self, **kwargs):
        """
        Create a deep copy of the Example instance, optionally updated with new or changed key-value pairs.

        Args:
            **kwargs: Key-value pairs to add to or update in the copy of the instance's store.

        Returns:
            Example: A new Example instance that is a copy of this instance with the specified updates.
        """
        return type(self)(base=self, **kwargs)

    def without(self, *keys):
        copied = self.copy()
        for key in keys:
            del copied[key]
        return copied
    
    def toDict(self):
        return self._store.copy()
