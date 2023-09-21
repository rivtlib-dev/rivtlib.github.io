"""check for init file and set defaults if not found"""

# config file
config = ConfigParser()
config.read(Path(prvP, "rivt.ini"))
reportS = config.get('report', 'title')
headS = config.get('md', 'head')
footS = config.get('md', 'foot')
divS = config.get("divisions", prfxS)
