import sys
import csv
import textwrap
import logging
import warnings


class Commands():
    """convert rivt commands to reST

    """

    def __init__(self, paramL, incrD, folderD,  localD):
        """convert rivt commands to md or reST

            ======================================================== ===========
                            command syntax                              scope
            ======================================================== ===========

            || append | folder | file1, file2, ...                         R
            || github | repository                                         R
            || project | file | type                                       R
            || image | folder | file1, file2  | size1, size2              I,V
            || table | folder | file  | max width | rows                  I,V
            || text | folder | file  | type                               I,V
            || declare | folder | file | type | rows                       V

        """

        self.localD = localD
        self.folderD = folderD
        self.incrD = incrD
        self.widthII = incrD["widthI"] - 1
        self.paramL = paramL
        self.errlogP = folderD["errlogP"]

        modnameS = __name__.split(".")[1]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")
