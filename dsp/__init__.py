from .modules import *
from .primitives import *
from .templates import *
from .utils import settings


"""
TODO:

The DspModule class serves as a proxy to our original 'dsp' module. It provides direct access to settings 
stored in `dsp_settings` as if they were top-level attributes of the 'dsp' module, while also ensuring that
all other regular attributes (like functions, classes, or submodules) of the 'dsp' module remain accessible.

By replacing the module's symbols with an instance of DspModule, we allow users to access settings 
with the syntax `dsp.<setting_name>` instead of the longer `dsp.dsp_settings.<setting_name>`. This makes 
for more concise and intuitive code. However, due to its unconventional nature, developers should be 
careful when modifying this module to ensure they maintain the expected behavior and access patterns.
"""


"""

class DspModule:
    '''A proxy class for the original 'dsp' module providing direct access to settings.

    This class allows users to access settings from `dsp_settings` using the simpler syntax `dsp.<setting_name>`.
    It also maintains access to all other attributes (functions, classes, submodules) of the 'dsp' module.

    Note that developers should handle modifications to this class with care to preserve its intended access patterns.
    '''
    
    def __init__(self):
        '''Initializes the DspModule by importing and storing the original module object.'''
        # Import and store the original module object
        self._original_module = sys.modules[__name__]
    
    def __getattr__(self, name):
        '''Attempts to get an attribute from the original module or `dsp_settings`.

        If the attribute is not part of the original module or `dsp_settings`, an AttributeError is raised.

        Args:
            name (str): The name of the attribute to retrieve.

        Returns:
            Any: The value of the attribute found in the original module or `dsp_settings`.

        Raises:
            AttributeError: If the module and `dsp_settings` have no such attribute.
        '''
        
        if hasattr(self._original_module, name):
            return getattr(self._original_module, name)
        
        # Next, check dsp_settings
        if hasattr(dsp_settings, name):
            return getattr(dsp_settings, name)
        
        raise AttributeError(f"'{type(self).__name__}' object and the original module have no attribute '{name}'")

import sys
sys.modules[__name__] = DspModule()

"""