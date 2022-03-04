from time import sleep
from model.classes.provider import Provider
from view import main as mainview
from controller import user as uc, admin as ac, product as pc, provider as prc
from model.classes import user as user
from extra import random as r

db = "./model/app.db"


# admin = ac.DatabaseController(db)
# prov = prc.ProviderController(db)
# admin.init_database()
# admin.populate_database()

# # print(c)
# # for p in provs:
# #     print(p, "\n")

# c = uc.UserController(db)
# classes = r.RandomObjectInfo(db)
# usr = classes.Customer()
# customer = user.Customer(usr[0], usr[1], usr[2], usr[3], usr[4], usr[5], usr[6], usr[7])

# input("Selecionar todos os produtos")
# p = pc.ProductController(db)
# products = p.select_all_products()
# for product in products:
#     print(product)
# c.insert_user(customer)


# # input("Produtos mais vendidos")
# # print(p.select_most_sold_products())


# input("Todos os clientes")
u = uc.UserController(db)
# customers = u.select_all_customers()
# for customer in customers:
#     print(customer)

# input("Todos os vendedores")
# sellers = u.select_all_sellers()
# for seller in sellers:
#     print(seller)

# input("Melhor vendedor do mês: ")
# print(u.select_best_seller_of_the_month(1, 2022))


mainview.MainView()
