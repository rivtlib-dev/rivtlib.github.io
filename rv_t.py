#!python
"T2utf and T2rst classes"


class T2utf:
    """convert insert-string to UTF8 calc"""

    def __init__(self, strL: list, folderD, cmdD, sectD):
        """convert insert-string to UTF8 calc-string

        Args:
            strL (list): calc lines
            folderD (dict): folder paths
            cmdD (dict): command settings
            sectD (dict): section settings
        """

        self.utfS = """"""  # utf calc string
        self.strL = strL
        self.folderD = folderD
        self.sectD = sectD
        self.cmdD = cmdD

    def t_rst(self) -> tuple:
        """parse table-strings

        Return:
            calcS (list): utf formatted calc-string (appended)
            setsectD (dict): section settings
            setcmdD (dict): command settings
            rivtD (list): calculation values
        """

        tcmdL = ["text", "table", "image"]
        tmethL = [self._itext, self._itable, self._iimage]

        self._parseUTF("table", tcmdL, tmethL, ttagL)

        return self.calcS, self.setsectD, self.setcmdD, self.rivtD
