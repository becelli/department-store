from xmlrpc.client import MAXINT
from view.gui import GUI
from controller import user as uc, admin as ac, product as pc, provider as prc
from model.classes import user as user
import random as rd

db = f"./model/database/app{rd.randint(0, MAXINT)}.db"
db = f"./model/database/app.db"

admin = ac.DatabaseController(db)
admin.init_database()
# admin.populate_database()
GUI(db)
