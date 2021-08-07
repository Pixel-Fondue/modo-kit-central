# python

import lx, lxu, modo
import com_hub as hub

Command_Name = "modo.Community.Hub"


class Modo_Community_Hub_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Release ID", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Quick Clips ID", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("Page ID", lx.symbol.sTYPE_INTEGER)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'Open Modo QuickClips and Tutorial Videos'

    def cmd_Desc(self):
        return 'Open the QuickClips - Tutorial Videos using ID integer as argument to filter by Modo Releases defined in Menu.'

    def cmd_Tooltip(self):
        return 'Open the QuickClips - Tutorial Videos using ID integer as argument to filter by Modo Releases defined in Menu.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'Open Modo QuickClips and Tutorial Videos'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        args = lx.args()
        lx.out(args)
        RELEASE_ID = self.dyna_Int(0)
        QC = self.dyna_Bool(1)
        PAGE_ID = self.dyna_Int(2)

        QUALITY = lx.eval('user.value SMO_UseVal_MODO_COMU_HUB_VideoQuality ?')
        lx.out('YouTube Video Quality:', QUALITY)
        FULLSCREEN = lx.eval('user.value SMO_UseVal_MODO_COMU_HUB_FullScreen ?')
        lx.out('Open YouTube Page in Fullscreen Mode:', FULLSCREEN)
        YouTube = "https://www.youtube.com/"

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

        ##################
        ####### --> 15 . 1
        ### - Quick Clips
        if RELEASE_ID == 1510 and QC:
            if PAGE_ID == 1:
                # Modo 15.1 - Workflow Refined
                URL = "zbQN4sf_hh0"

            if PAGE_ID == 2:
                # Modo 15.1 - Never Leave the Viewport Again and Speed up Your Workflow with OmniHaul
                URL = "PBHgc9jnJ5g"

            if PAGE_ID == 3:
                # Modo 15.1 - Create Complex Models Easily With Curve Booleans
                URL = "NJnJ25zRTf8"

            if PAGE_ID == 4:
                # Modo 15.1 - Streamline your Procedural Workflow with the MeshOp Stack Node
                URL = "imVZd5xe_uw"

            if PAGE_ID == 5:
                # Modo 15.1 - Improve Performance in Modo with Deferred Evaluations
                URL = "vwl8BjylhA0"

            if PAGE_ID == 6:
                # Modo 15.1 - Refract Light and Look Around in the Viewport with mPath Improvements
                URL = "WaOG1wVkpUw"

            if PAGE_ID == 7:
                # Modo 15.1 - Clean up Heavy Scenes Quickly and Easily with Static Analysis
                URL = "tpi8nq_5k0o"

            if PAGE_ID == 8:
                # Modo 15.1 - Making Precision Modeling Easy
                URL = "ChgWxsifq1c"

            if PAGE_ID == 9:
                # Modo 15.1 - Tile UVs and Scale to Real World Size with File I/O Enhancements
                URL = "pJMYGLRBWmk"

        ### - Tutorials
        if RELEASE_ID == 1510 and not QC:
            if PAGE_ID == 1:
                # Modo 15.1 - Create Complex 3D Shapes from 2D Curves with Curve Booleans
                URL = "kjAfnan-ha0"

            if PAGE_ID == 2:
                # Modo 15.1 - Cut Down Waiting Times With Mesh Stack Evaluations
                URL = "uHFpiJjZTPE"

            if PAGE_ID == 3:
                # Modo 15.1 - Speed up Your Workflow With OmniHaul
                URL = "JemSBlPJpC8"

        ##################
        ####### --> 15 . 0
        ### - Quick Clips
        if RELEASE_ID == 1500 and QC == True:
            if PAGE_ID == 1:
                # Modo 15.0 - Mesh Fusion - UI Updates
                URL = "d_s2IVkuubU"

            if PAGE_ID == 2:
                # Modo 15.0 - Mesh Fusion - Select Source Mode
                URL = "x8fDjz59rQM"

            if PAGE_ID == 3:
                # Modo 15.0 - Mesh Fusion - Edit Attribute Mode
                URL = "Quz1R6sdLgg"

            if PAGE_ID == 4:
                # Modo 15.0 - Mesh Fusion - Technology Enhancements
                URL = "VhsKgYIi88w"

            if PAGE_ID == 5:
                # Modo 15.0 - Animation Editor
                URL = "dAYaVglSpZs"

            if PAGE_ID == 6:
                # Modo 15.0 - Rig Clay Enhancements
                URL = "XIjS-aC39ek"

            if PAGE_ID == 7:
                # Modo 15.0 - Modeling Enhancements
                URL = "bD0Q4sDMymc"

            if PAGE_ID == 8:
                # Modo 15.0 - Procedural Modeling Enhancements
                URL = "HgigC7wOp0Q"

            if PAGE_ID == 9:
                # Modo 15.0 - AVP Depth of Field
                URL = "FN3_UcOZWB0"

            if PAGE_ID == 10:
                # Modo 15.0 - Python Support
                URL = "XfH-F1eIabw"

            if PAGE_ID == 11:
                # Modo 15.0 - Tune Ups
                URL = "WOrf-RWldYg"

        ##################
        ####### --> 14 . 2
        ### - Quick Clips
        if RELEASE_ID == 1420 and QC == True:
            if PAGE_ID == 1:
                # Modo 14.2 - Overview
                URL = "Hty8DuCXA08"

            if PAGE_ID == 2:
                # Modo 14.2 - Rig Clay
                URL = "AXGNQcAUPmo"

            if PAGE_ID == 3:
                # Modo 14.2 - AVP Enhancements
                URL = "6NP-WSqgNVc"

            if PAGE_ID == 4:
                # Modo 14.2 - Edge Chamfer Enhancements
                URL = "https://vimeo.com/478860419"

            if PAGE_ID == 5:
                # Modo 14.2 - Solo Command
                URL = "XeD3FWNxbyw"

            if PAGE_ID == 6:
                # Modo 14.2 - Procedural Vertex Map Operations
                URL = "Q5AC8m8N20I"

            if PAGE_ID == 7:
                # Modo 14.2 - MeshFusion: Sharp Bezier Corners
                URL = "JBb0pvZN1Hw"

            if PAGE_ID == 8:
                # Modo 14.2 - Modeling Enhancements
                URL = "uVze9k0EFlw"

            if PAGE_ID == 9:
                # Modo 14.2 - Cryptomatte
                URL = "RnhCAW9MTU4"

            if PAGE_ID == 10:
                # Modo 14.2 - Workflow and User Experience
                URL = "NimXWp7esFw"

            if PAGE_ID == 11:
                # Modo 14.2 - Performance Improvements
                URL = "GskFvwxaJwA"

            if PAGE_ID == 12:
                # Modo 14.2 - UV Enhancements
                URL = "tHeSYlrAa7o"

        ##################
        ####### --> 14 . 1
        ### - Quick Clips
        if RELEASE_ID == 1410 and QC == True:
            if PAGE_ID == 1:
                # Modo 14.1 - Workflow Enhanced
                URL = "iquqWRFoPOw"

            if PAGE_ID == 2:
                # Modo 14.1 - AVP Improvements
                URL = "BCbL-ncwyX0"

            if PAGE_ID == 3:
                # Modo 14.1 - Rigging Improvements
                URL = "V1RCVsM5vmg"

            if PAGE_ID == 4:
                # Modo 14.1 - Bevel Auto Weld
                URL = "n3fOnWw4Fhg"

            if PAGE_ID == 5:
                # Modo 14.1 - UV Enhancements
                URL = "R2qF1sPqLqg"

            if PAGE_ID == 6:
                # Modo 14.1 - Modeling Enhancements
                URL = "nKCWLaHjnt4"

            if PAGE_ID == 7:
                # Modo 14.1 - Denoise Updates
                URL = "gr0BhDcTDxc"

            if PAGE_ID == 8:
                # Modo 14.1 - Rendering Enhancements
                URL = "gvAnGtk8iYw"

            if PAGE_ID == 9:
                # Modo 14.1 - PBR Loader
                URL = "BfXonhSii4w"

            if PAGE_ID == 10:
                # Modo 14.1 - Performance Improvements
                URL = "xHTgpoajwCg"

            if PAGE_ID == 11:
                # Modo 14.1 - USD Importer
                URL = "RGWXNvc_UXI"

            if PAGE_ID == 12:
                # Modo 14.1 - Curve Sweep
                URL = "PwNdU5a09oo"

            if PAGE_ID == 13:
                # Modo 14.1 - IK/FK Matching
                URL = "rIqG0w_MFfs"

            if PAGE_ID == 14:
                # Modo 14.1 - Disable IK
                URL = "KbVvrPT4Qbc"

            if PAGE_ID == 15:
                # Modo 14.1 - AVP Performance
                URL = "yS1sdXT09n8"

        ##################
        ####### --> 14 . 0
        ### - Quick Clips
        if RELEASE_ID == 1400 and QC == True:
            if PAGE_ID == 1:
                # Modo 14.0 - Workflow Enhanced
                URL = "csuM8nuP4jk"

            if PAGE_ID == 2:
                # Modo 14.0 - Ghost and Xray Modes
                URL = "jhPZKC_Kbjg"

            if PAGE_ID == 3:
                # Modo 14.0 - Unbevel and Add Point
                URL = "gJvJNeNToIs"

            if PAGE_ID == 4:
                # Modo 14.0 - Edge Chamfer
                URL = "sAqNBuJQZ6k"

            if PAGE_ID == 5:
                # Modo 14.0 - Face Slide Mode
                URL = "-HUXhYCFDRg"

            if PAGE_ID == 6:
                # Modo 14.0 - Scale Texture Groups
                URL = "1vBkoEZZQOY"

            if PAGE_ID == 7:
                # Modo 14.0 - Procedural Vertex Maps
                URL = "MemMlKdyYP8"

            if PAGE_ID == 8:
                # Modo 14.0 - MeshFusion Embossing
                URL = "0efarjxVuVA"

            if PAGE_ID == 9:
                # Modo 14.0 - UV Enhancements
                URL = "NrASEZk5Vz0"

            if PAGE_ID == 10:
                # Modo 14.0 - Markup
                URL = "cbh4y96tXtw"

            if PAGE_ID == 11:
                # Modo 14.0 - mPath Renderer Enhancements
                URL = "spbnlHZaglA"

            if PAGE_ID == 12:
                # Modo 14.0 - General Enhancements
                URL = "oOvNgvVyukw"

        if RELEASE_ID == 1420 and PAGE_ID == 4 and QC == True:
            Output_URL = URL

        else:
            Output_URL = YouTube + Watch + URL + VidQua + FullS
        lx.eval('openURL {%s}' % Output_URL)


lx.bless(Modo_Community_Hub_Cmd, Command_Name)
