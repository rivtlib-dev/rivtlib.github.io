# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + baseS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogP,
    filemode="w")
docshortP = Path(*Path(docP).parts[-2:])
bakshortP = Path(*Path(bakP).parts[-2:])


if docP.exists():
    logging.info(f"""rivt file : [{docS}]""")
    logging.info(f"""rivt path : [{docP}]""")
    print(f"""rivt short path : [{docshortP}]""")
else:
    logging.info(f"""rivt file path not found: {docP}""")

# write backup doc file
with open(rivtP, "r") as f2:
    rivtS = f2.read()
    rivtL = f2.readlines()
with open(bakP, "w") as f3:
    f3.write(rivtS)
logging.info(f"""rivt backup: [{bakshortP}]""")
print(" ")

with open(rivtP, "r") as f1:
    rivtS = f1.read()
    rivtS += rivtS + """\nsys.exit()\n"""
