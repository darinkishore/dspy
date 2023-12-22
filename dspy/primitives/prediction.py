from dspy.primitives.example import Example


class Prediction(Example):
    """
    The Prediction class is a subclass of the Example class.
    It enhances an Example instance with functionality specific to model predictions, such as managing multiple completions.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of the Prediction class with properties inherited from Example, while removing properties that are not applicable to Prediction (`_demos` and `_input_keys`).

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        
        del self._demos
        del self._input_keys

        self._completions = None
    
    @classmethod
    def from_completions(cls, list_or_dict, signature=None):
        """
        Create a new instance of the Prediction class from provided completions, which can be a list or dictionary representing the model's output.

        Each completion will be stored inside the `_completions` property, and the first set of completions will be expanded into the `_store` of the Prediction.

        Args:
            list_or_dict (list or dict): The completions to use for creating the Prediction instance.
            signature (str, optional): The signature of the completions. Defaults to None.

        Returns:
            Prediction: A new instance of the Prediction class.
        """
        obj = cls()
        obj._completions = Completions(list_or_dict, signature=signature)
        obj._store = {k: v[0] for k, v in obj._completions.items()}

        return obj
    
    def __repr__(self):
        """
        Generate a string representation of the Prediction instance that includes the contents of `_store` and represents the quantity of multiple completions if they exist.

        The method intelligently omits detailed presentation of all completions for the sake of brevity when there are multiple completions available.

        Returns:
            str: A string representation of the Prediction instance.
        """
        store_repr = ',\n    '.join(f"{k}={repr(v)}" for k, v in self._store.items())

        if self._completions is None or len(self._completions) == 1:
            return f"Prediction(\n    {store_repr}\n)"
        
        num_completions = len(self._completions)
        return f"Prediction(\n    {store_repr},\n    completions=Completions(...)\n) ({num_completions-1} completions omitted)"
        
    def __str__(self):
        """
        Generate a string representation of the Prediction instance, effectively delegating to the `__repr__` method.

        This provides consistency between `str` and `repr` outputs for the Prediction object.

        Returns:
            str: A string representation of the Prediction instance.
        """
        return self.__repr__()

    @property
    def completions(self):
        """
        Access the `Completions` object associated with the Prediction instance.

        Returns the `_completions` attribute which encapsulates all completions of the Prediction.

        Returns:
            Completions: The completions of the Prediction instance.
        """
        return self._completions


class Completions:
    def __init__(self, list_or_dict, signature=None):
        """
        Construct a Completions object to manage multiple potential results (completions) of a prediction.

        The constructor takes either a list of dictionaries, each representing a distinct completion, or a single dictionary
        with keys mapping to lists of possible values. It validates consistency and uniformity of completion lengths.

        Args:
            list_or_dict (list|dict): Input data representing completions, either as a list of option dicts or a dict of option lists.
            signature (str|None, optional): A unique identifier for the set of completions, commonly used to associate it with a specific model or model state.

        Raises:
            AssertionError: If the input is not in the correct format (list of dicts or dict of lists with consistent lengths).
        """
        self.signature = signature

        if isinstance(list_or_dict, list):
            kwargs = {}
            for arg in list_or_dict:
                for k, v in arg.items():
                    kwargs.setdefault(k, []).append(v)
        else:
            kwargs = list_or_dict

        assert all(isinstance(v, list) for v in kwargs.values()), "All values must be lists"

        if kwargs:
            length = len(next(iter(kwargs.values())))
            assert all(len(v) == length for v in kwargs.values()), "All lists must have the same length"

        self._completions = kwargs

    def items(self):
        return self._completions.items()

    def __getitem__(self, key):
        if isinstance(key, int):
            """
            Retrieve an individual Prediction instance by index from a collection of completions.

            This method facilitates accessing one of the several possible completions based on an index, imitating list access semantics.

            Args:
                key (int): The index of the desired completion.

            Returns:
                Prediction: The Prediction object corresponding to the specified index.

            Raises:
                IndexError: If the index provided is not within the bounds of the completion options.
            """
            if key < 0 or key >= len(self):
                raise IndexError("Index out of range")
            
            return Prediction(**{k: v[key] for k, v in self._completions.items()})
        
        return self._completions[key]

    def __getattr__(self, name):
        """
        Offer attribute-style access to the lists of completion values associated with a given attribute name.

        This method provides a convenient way to access completion values that are stored as lists under specific attribute names.

        Args:
            name (str): The name of the attribute to access.

        Returns:
            list: A list of values corresponding to the requested attribute name.

        Raises:
            AttributeError: If the requested attribute name is not amongst the available completions.
        """
        if name in self._completions:
            return self._completions[name]
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __len__(self):
        # Return the length of the list for one of the keys
        """
        Calculate the number of individual completion options available.

        This method assumes uniform length of completion lists and provides the count of how many distinct completions exist.

        Returns:
            int: The count of completion options.
        """
        # It assumes all lists have the same length
        return len(next(iter(self._completions.values())))

    def __contains__(self, key):
        return key in self._completions
        """
        Determine if a given key is part of the available completions.

        This method checks for the presence of a key within the completion data, indicating if there are any values associated with that key in the completions.

        Args:
            key (str): The key to check for.

        Returns:
            bool: True if the key is present, False otherwise.
        """

    def __repr__(self):
        items_repr = ',\n    '.join(f"{k}={repr(v)}" for k, v in self._completions.items())
        return f"Completions(\n    {items_repr}\n)"
        """
        Represent the Completions object in a readable format, listing key-value pairs.

        Generates a string representation that enumerates all completions with their associated values, presented in a structured format for better readability.

        Returns:
            str: The string representation of the Completions object.
        """

    def __str__(self):
        # return str(self._completions)
        """
        Provide the string representation of the Completions, which is defined to be identical to the `__repr__` output.

        This ensures consistent display of the Completions object regardless of whether it's printed or inspected.

        Returns:
            str: The string representation of the Completions object.
        """
        return self.__repr__()
