"""check for init file and set defaults if not found"""

from configparser import ConfigParser

# config file
config = ConfigParser()
config.read(Path(prvP, "rivt.ini"))
reportS = config.get('report', 'title')
headS = config.get('md', 'head')
footS = config.get('md', 'foot')
divS = config.get("divisions", prfxS)
