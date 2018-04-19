"""
Config is for all the particular setup details such as
the app environment, database name and ip, super user account
details, etc...
"""
import json
import logging
import os
import sys


class OVSConfig:
    """
    Used to load config from a file.

    Args:
        config_path: A path to a json file with the app's configuration.
                                     If none is provided 'config/config-local-dev.json' will be used.

    Examples:
        config = OVSConfig('config/config-local-dev.json')
        print(config['database'])

    Returns:
        A OVSConfig representing the fields in the JSON file given by config_path.
    """

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = 'config/config-local-dev.json'

        assert os.path.exists(config_path)

        with open(config_path) as config_file:
            try:
                self._config = json.load(config_file)
            except ValueError:
                logging.exception('Error reading config file %s', config_file)
                sys.exit(1)

    def __getitem__(self, item):
        return self._config[item]

    def __contains__(self, item):
        return item in self._config

    def __setitem__(self, key, value):
        raise Exception('OVSConfig is static, and cannot be edited.')

    def get(self, key, default_value):
        """
        Fetch the value associate with the key in the dictionary.

        Args:
            key: The key to access the dictionary.
            default_value: The default value if the key is not mapped.

        Returns:
            The value associated with the key or default if key is not mapped.
        """
        if key in self._config:
            return self._config[key]

        return default_value

    def items(self):
        """
        Fetch all dictionary items.

        Returns:
            A list of key, value tuples.
        """
        return self._config.items()
