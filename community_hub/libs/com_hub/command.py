from operator import ior
from functools import reduce

from lx.symbol import fCMDARG_OPTIONAL, fCMDARG_QUERY
from lxu.command import BasicCommand


class hubCommand(BasicCommand):

    def add_arg(self, name, arg_type, optional=True, query=False):
        self.dyna_Add(name, arg_type)
        current_id = self.arg_id
        flags = list()
        if optional:
            flags.append(fCMDARG_OPTIONAL)
        if query:
            flags.append(fCMDARG_QUERY)

        self.dyna_SetFlags(current_id, reduce(ior, flags))
        self.arg_id += 1

        return current_id