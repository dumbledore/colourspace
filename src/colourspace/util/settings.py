# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import builtins
import pickle

from logging import getLogger

# See: https://docs.python.org/3/library/pickle.html#restricting-globals


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        safe_builtins = {
            'range',
            'complex',
            'set',
            'frozenset',
            'slice',
        }

        # Only allow safe classes from builtins.
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)

        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" % (module, name))


class Settings:
    def __init__(self, filename):
        self._filename = filename

    def get(self, setting, default=None):
        try:
            with open(self._filename, "rb") as f:
                # Load the dict data from the store
                data = RestrictedUnpickler(f).load()

                # Return the setting value (if there)
                return data.get(setting, default)
        except:
            getLogger(__name__).warning(
                f"Could not read from settings file {self._filename}", exc_info=True)
            return default

    def set(self, setting, value):
        # Have an empty default in case reading fails
        data = {}

        try:
            with open(self._filename, "rb") as f:
                # Load the dict data from the store
                data = RestrictedUnpickler(f).load()
        except:
            getLogger(__name__).warning(
                f"Could not read from settings file {self._filename}", exc_info=True)

        # Update the data
        data[setting] = value

        try:
            with open(self._filename, "wb") as f:
                # Save to the file
                pickle.dump(data, f)
        except:
            getLogger(__name__).warning(
                f"Could not write to settings file {self._filename}", exc_info=True)

    def remove(self, setting):
        try:
            with open(self._filename, "rb") as f:
                # Load the dict data from the store
                data = RestrictedUnpickler(f).load()

            if setting in data:
                del data[setting]

                with open(self._filename, "wb") as f:
                    # Save to the file
                    pickle.dump(data, f)
        except:
            getLogger(__name__).warning(
                f"Could not update settings file {self._filename}", exc_info=True)
