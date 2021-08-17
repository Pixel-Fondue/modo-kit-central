import lx
import lxu
import com_hub
from com_hub.command import hubCommand
from com_hub.gui import CommunityHub


class HubLauncher_cmd(hubCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        """Modo Override: Set the internal flags of the command.

        Notes:
            No need to undo or show the command in the event log so we run it silently.

        Returns:
            (int): The quiet flag
        """
        return lx.symbol.fCMD_QUIET

    def basic_Execute(self, msg, flags):
        """Modo Override: Launches the Material Search window.

        Args:
            msg (lx.object.Message): The commands message object
            flags (int): The int result of cmd_Flags()
        """
        if com_hub.hub_window:
            com_hub.hub_window.show()
        else:
            com_hub.hub_window = CommunityHub()


lx.bless(HubLauncher_cmd, "com.hub")
