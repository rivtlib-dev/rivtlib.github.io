"""parse rivtlib folder structure"""


def get_div_files(cur_dirP):
    """list of rivt file paths in div
    """

    docpathP = Path(os.getcwd())
    for fileS in os.listdir(docpathP):
        # print(fileS)
        if fnmatch.fnmatch(fileS, "rivt??-*.py"):
            docfileS = fileS
            docP = Path(docpathP, docfileS)
            # print(docP)
            break
    if docfileS == "xx":
        print("INFO     rivt file not found")
        exit()

# find data and function file
# dataP = Path(fnmatch.fnmatch(argfileS, "rivt??-*.py"))
