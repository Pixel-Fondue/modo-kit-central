from operator import ior
from functools import reduce

import lx
from lxu.command import BasicCommand


class hubCommand(BasicCommand):
    """Command wrapper to add an index return when adding an argument."""

    def add_arg(self, name, arg_type, optional=True, query=False):
        """Adds an argument to the command and returns it's index.

        Args:
            name (str): The name of the argument.
            arg_type (str): The string type of the argument.
            optional (bool): If the argument is optional.
            query (bool): If the argument is queryable.

        Returns:
            current_id (int): The index of the newly added argument.
        """
        self.dyna_Add(name, arg_type)
        current_id = self.arg_id
        flags = list()
        if optional:
            flags.append(lx.symbol.fCMDARG_OPTIONAL)
        if query:
            flags.append(lx.symbol.fCMDARG_QUERY)

        # Add flags to argument. reduce with ior == flag | flag | ...
        self.dyna_SetFlags(current_id, reduce(ior, flags))
        self.arg_id += 1

        return current_id
