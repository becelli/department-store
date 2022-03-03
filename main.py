from view import main as mainview
from controller import user as uc, admin as ac
from model.classes import user as user
from extra import random as r

db = "./model/app.db"


admin = ac.DatabaseController(db)
admin.init_database()
admin.populate_database()

c = uc.UserController(db)
classes = r.RandomObjectInfo(db)
usr = classes.Customer()
customer = user.Customer(usr[0], usr[1], usr[2], usr[3], usr[4], usr[5], usr[6], usr[7])

# c.insert_user(customer)

# mainview.MainView()
