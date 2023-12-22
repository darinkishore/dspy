import copy
import ujson


class BaseModule:
    """
    Base class for all modules in the DSPy framework.

    Provides functionalities common to all module classes such as parameter handling,
    creating deep copies, and saving or loading module states.
    """

    def __init__(self):
        """
        Initialize a new instance of the BaseModule class.
        """
        pass

    def named_parameters(self):
        """
        Get the named parameters of the module.

        Unlike PyTorch, this method also handles (non-recursive) lists of parameters.

        Returns:
            list: A list of tuples, where each tuple contains the name of a parameter and the parameter itself.
        """

        from dspy.predict.parameter import Parameter

        visited = set()
        named_parameters = []

        def add_parameter(param_name, param_value):
            if isinstance(param_value, Parameter) and id(param_value) not in visited:
                visited.add(id(param_value))
                named_parameters.append((param_name, param_value))

        # Iterate over all attributes of the instance, extracting named parameters
        for name, value in self.__dict__.items():
            if isinstance(value, Parameter):
                add_parameter(name, value)

            elif isinstance(value, BaseModule):
                # When a sub-module is pre-compiled, keep it frozen.
                if not value._compiled:
                    for sub_name, param in value.named_parameters():
                        add_parameter(f"{name}.{sub_name}", param)
            
            elif isinstance(value, (list, tuple)):
                for idx, item in enumerate(value):
                    add_parameter(f"{name}[{idx}]", item)

            elif isinstance(value, dict):
                for key, item in value.items():
                    add_parameter(f"{name}['{key}']", item)

        return named_parameters

    def parameters(self):
        """
        Retrieve all the parameters of the module as a flat list.

        This method simplifies accessing all parameters by returning them without their names,
        making it useful for operations that don't require named parameter information.

        Returns:
            list: A list of parameters.
        """
        return [param for _, param in self.named_parameters()]

    def deepcopy(self):
        """
        Create a deep copy of the module.

        Returns:
            BaseModule: A deep copy of the module.
        """
        return copy.deepcopy(self)

    def reset_copy(self):
        """
        Create a reset copy of the module with all parameters restored to their initial state.

        This method duplicates the module, and then resets all parameters to their original states,
        as defined by their respective reset logic, effectively 'reinitializing' them.

        Returns:
            BaseModule: A reset copy of the module.
        """
        obj = copy.deepcopy(self)
        
        for param in obj.parameters():
            param.reset()
        
        return obj
    
    def dump_state(self):
        """
        Dump the state of the module.

        Returns:
            dict: A dictionary representing the state of the module.
        """
        return {name: param.dump_state() for name, param in self.named_parameters()}
    
    def load_state(self, state):
        """
        Restore the state of the module from a given dictionary of parameter states.

        This method takes a dictionary where keys match parameter names and values are
        their associated states, and applies these states to the corresponding parameters
        within the module.

        Args:
            state (dict): A dictionary representing the state of the module.
        """
        for name, param in self.named_parameters():
            param.load_state(state[name])
    
    def save(self, path):
        """
        Save the state of the module to a file.

        Args:
            path (str): The path to the file where the state should be saved.
        """
        with open(path, "w") as f:
            f.write(ujson.dumps(self.dump_state(), indent=2))
    
    def load(self, path):
        """
        Load the state of the module from a file.

        Args:
            path (str): The path to the file from which the state should be loaded.
        """
        with open(path, "r") as f:
            self.load_state(ujson.loads(f.read()))
