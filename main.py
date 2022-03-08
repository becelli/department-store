from time import sleep
from xmlrpc.client import MAXINT
from view.gui import GUI
from controller import user as uc, admin as ac, product as pc, provider as prc
from model.classes import user as user
from extra import random as r
import random as rd

db = f"./model/database/app{rd.randint(0, MAXINT)}.db"

admin = ac.DatabaseController(db)
admin.init_database()
admin.populate_database()
GUI(db)

# prov = prc.ProviderController(db)

# provs = prov.get_all_providers()
# for p in provs:
#     print(p, "\n")

# c = uc.UserController(db)
# classes = r.RandomObjectInfo(db)
# usr = classes.Customer()
# customer = user.Customer(usr[0], usr[1], usr[2], usr[3], usr[4], usr[5], usr[6], usr[7])
# c.insert_user(customer)

# p = pc.ProductController(db)
# input("Selecionar todos os produtos")
# products = p.select_all_products()
# for product in products:
# print(product)


# # input("Produtos mais vendidos")
# print(p.select_most_sold_products())


# input("Todos os clientes")
# customers = c.get_all_customers()
# for customer in customers:
# print(customer)
#
# input("Todos os vendedores")
# sellers = c.get_all_sellers()
# for seller in sellers:
#     print(seller)

# input("Melhor vendedor do mês: ")
# print(c.get_best_seller_of_the_month(1, 2022))
