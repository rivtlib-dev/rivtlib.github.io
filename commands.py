import sys
import csv
import textwrap
import logging


class Commands():
    """subclass - convert rivt commands to MD and reST

        ======================================================== ===========
                        command syntax                              scope
        ======================================================== ===========

        || append | folder | file1, file2, ...                         R
        || github | folder | file |repository                          R
        || project | file | type                                       R
        || image | folder | file1, (file2)  | size1, (size2)          I,V
        || table | folder | file  | max width | rows                  I,V
        || text | folder | file  | type                               I,V
        || declare | folder | file | rows                              V
        || assign | folder | file | rows                               V

        """

    def cmd_parse(self, cmdS):
        """_summary_
        """
        self.cmdS = cmdS
        return eval("self." + cmdS+"()")

    def append(self):
        """_summary_
        """
        pass

    def github(self):
        """_summary_
        """
        pass
