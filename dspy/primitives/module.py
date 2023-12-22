import copy
import ujson


class BaseModule:
    """
    Base class for all modules in DSPy providing common interfaces and behaviors.

    The BaseModule serves as a foundation for creating complex modules that may contain
    parameters, sub-modules, and custom behaviors during training and inference.
    """

    def __init__(self):
        """
        Initializes a new BaseModule instance.

        This constructor sets up the basic structure for further customization in derived module classes.
        """
        pass

    def named_parameters(self):
        """
        Retrieves a list of tuples, each containing the name and value of a parameter.
        
        This method returns named parameters for the module itself and any sub-modules, including parameters
        contained within non-recursive lists, tuples, and dictionaries.

        Returns:
            List[Tuple[str, Parameter]]: A list of tuples, where each tuple contains the name of a parameter and the parameter itself.
        """

        from dspy.predict.parameter import Parameter

        visited = set()
        named_parameters = []

        def add_parameter(param_name, param_value):
            if isinstance(param_value, Parameter) and id(param_value) not in visited:
                visited.add(id(param_value))
                named_parameters.append((param_name, param_value))

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
        Get the parameters of the module.

        Returns:
            list: A list of parameters.
        """
        return [param for _, param in self.named_parameters()]

    def deepcopy(self):
        """
        Creates a fully independent deep copy of the module and its associated sub-modules and parameters.

        This is useful for creating separate instances of a module for different tasks or datasets.

        Returns:
            BaseModule: A new instance of the module with all internal elements deep-copied.
        """
        return copy.deepcopy(self)

    def reset_copy(self):
        """
        Creates a deep copy of the module with reset parameters.
        
        Each parameter within the copy is reset back to its initial state.

        Returns:
            BaseModule: A new instance of the module with reset parameters.
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
        Load the state of the module from a dictionary.

        Args:
            state (dict): A dictionary representing the state of the module.
        """
        for name, param in self.named_parameters():
            param.load_state(state[name])
    
    def save(self, path):
        """
        Saves the current state of the module as a JSON representation to the specified file.
        
        The saved state includes the states of all module parameters.

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
