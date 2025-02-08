import lx

from mkc.command import MKCCommand


class MKCDebugCMD(MKCCommand):
    """Command to launch the Modo Kit Central window."""
    arg_id = 0  # Class variable to track the argument index

    def __init__(self) -> None:
        """Initialization of the Modo Kit Central Launcher command."""
        super().__init__()
        # Add port number argument for connecting to PyCharm debugger.
        self.port_id = self.add_arg("port", lx.symbol.sTYPE_INTEGER)

    def cmd_Flags(self) -> int:
        """Modo Override: Set the internal flags of the command.

        Notes:
            No need to undo or show the command in the event log, so we run it silently.

        Returns:
            The quiet flag
        """
        return lx.symbol.fCMD_QUIET

    def basic_Execute(self, msg: lx.object.Message, flags: int) -> None:
        """Modo Override: Launches the Material Search window.

        Args:
            msg: The commands message object
            flags: The int result of cmd_Flags()
        """
        # Get the port argument
        port = self.dyna_Int(self.port_id)

        import pydevd_pycharm
        pydevd_pycharm.settrace('localhost', port=port, stdoutToServer=True, stderrToServer=True)


lx.bless(MKCDebugCMD, "mkc.debug")
