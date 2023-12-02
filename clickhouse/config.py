import logging
import os

class ConfigBuilder:

    __slots__ = [
        "PREFIX",
        "USE_PREFIX",
        "ENV_KEYS",
        "LOGGER"
    ]
    
    def __init__(self, prefix: str = "CONFIG", use_prefix: bool = True) -> None:
        """
        The function initializes an object with a prefix and a flag to indicate whether to use the
        prefix, and then populates the environment variables and sets up a logger.
        
        :param prefix: The `prefix` parameter is a string that represents the prefix to be used for
        environment variables. It is used to differentiate environment variables specific to this code
        from other environment variables, defaults to CONFIG
        :type prefix: str (optional)
        :param use_prefix: The `use_prefix` parameter is a boolean flag that determines whether or not
        to use the `prefix` value when populating the environment variables. If `use_prefix` is set to
        `True`, the `prefix` value will be used as a prefix for the environment variable names. If `use,
        defaults to TRUE
        :type use_prefix: bool (optional)
        """
        self.PREFIX = prefix
        self.USE_PREFIX = use_prefix
        self.LOGGER = logging.getLogger(self.__class__.__qualname__)
        self._populate_env()

    def _get_config_keys(self) -> list[str]:
        """
        The function `_get_config_keys` returns a list of keys that are not present in the
        `ConfigBuilder` class.
        :return: A list of strings representing the keys of the object's slots that are not present in
        the `ConfigBuilder` class's slots.
        """
        return [key for key in self.__slots__ if key not in ConfigBuilder.__slots__]
    
    def _clean_key_string(self, key:str) -> str:
        """
        The function `_clean_key_string` takes a string `key` as input and removes any characters that
        are not alphanumeric, underscore, or hyphen, and returns the cleaned string.
        
        :param key: The `key` parameter is a string that represents a key
        :type key: str
        :return: the cleaned key string.
        """

        def check(l: str) -> bool:
            """
            The function "check" checks if a given string is alphanumeric or contains only underscores or
            hyphens.
            
            :param l: The parameter `l` is a string that represents a character
            :type l: str
            :return: a boolean value. It returns True if the input string `l` is alphanumeric or if it is
            equal to either '_' or '-'. Otherwise, it returns False.
            """
            if l.isalnum() or l in ['_', '-']:
                return True
            return False
        
        key = ''.join([letter for letter in key if check(letter)])
        return key
    
    def _get_env_keys(self) -> list[str]:
        """
        The function `_get_env_keys` returns a list of environment variable keys, with an optional
        prefix.
        :return: a list of environment keys.
        """
        keys = [self._clean_key_string(key) for key in self._get_config_keys()]
        if self.USE_PREFIX:
            keys = [ f"{self.PREFIX}_{key}" for key in keys]
        return keys
        

    def _populate_env(self) -> None:
        """
        The function `_populate_env` populates environment variables and sets them as attributes in the
        class instance.
        """
        env_keys = self._get_env_keys()
        for key in env_keys:
            value = os.environ.get(key)
            if value is None or len(value) == 0:
                self.LOGGER.warning(f"Env var \"{key}\" is either empty or does not exist. This will be set to empty string.")
                value = ""
            attr = key
            if self.USE_PREFIX:
                attr = key.split(f"{self.PREFIX}_")[1]
            self.__setattr__(attr, value)