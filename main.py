from view import main as mainview
from controller import user as uc, admin as ac
from model.classes import user as user
from extra import random as r

db = "app.db"

admin = ac.DatabaseController(db)
admin.create_provider_tables()
admin.create_sale_tables()
admin.create_user_tables()
admin.create_product_tables()
admin.create_payment_method_tables()


# c = uc.UserController(db)
# classes = r.RandomObjectInfo(db)
# usr = classes.Customer()
# customer = user.Customer(usr[0], usr[1], usr[2], usr[3], usr[4], usr[5], usr[6], usr[7])

# c.insert_user(customer)

mainview.MainView()
