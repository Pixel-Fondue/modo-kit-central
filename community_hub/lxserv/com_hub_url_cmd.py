import lx
import lxu
from com_hub.command import hubCommand


class HubUrlLauncher_cmd(hubCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.release_id = self.add_arg("Release ID", lx.symbol.sTYPE_INTEGER)
        self.quick_id = self.add_arg("Quick Clips ID", lx.symbol.sTYPE_BOOLEAN)
        self.page_id = self.add_arg("Page ID", lx.symbol.sTYPE_INTEGER)

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
        RELEASE_ID = self.dyna_Int(self.release_id)
        QC = self.dyna_Bool(self.quick_id)
        PAGE_ID = self.dyna_Int(self.page_id)

        if QUALITY == 1080:
            VidQua = "&vq=hd1080"
        if QUALITY == 720:
            VidQua = "&vq=hd720"
        if FULLSCREEN:
            FullS = "&fs=1"
            Watch = "watch_popup?v="
        else:
            FullS = "&fs=0"
            Watch = "watch?v="