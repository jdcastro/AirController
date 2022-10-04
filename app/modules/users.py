import email
from unicodedata import name

class Users():
    instancias = 0

    def __init__(self, id: int, name: str, userName: str, email:str, password: str):
        self.id = int(id)
        self.name = name
        self.userName = userName
        self.email = email
        self.__password = password
        Users.instancias += 1

    def saludar(self):
        a = 8+ self.id
        print(a)

foo = Users(1, "Juan Mariano", "juand", "j@jdcastro.co", "pwd")
faa = Users(2, "Juan Mariano", "juand", "j@jdcastro.co", "pwd")
fee = Users(3, "Juan Mariano", "juand", "j@jdcastro.co", "pwd")
print(Users.instancias, foo.id)
print(faa.instancias, faa.id)
print(fee.instancias, fee.id)
