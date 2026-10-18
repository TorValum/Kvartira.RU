import sqlite3
import time

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
                self.__cur.execute(sql)
                res = self.__cur.fetchall()
                if res: return res
        except:
             print("ошибка чтения")

        return []
#'''
##хз спроси Акеева, что делает
#    def getStations(self, alias): 
#        try:
#            self.__cur.execute(f"SELECT StationId, StationName, url FROM stations WHERE StationId = '{alias}' LIMIT 1")
#            res = self.__cur.fetchone()
#            if res: 
#                return res
#        except sqlite3.Error as e:
#                print("Ошибка чтения из БД"+str(e))#
#
#        return (False, False)
#'''
##Запрос вытаскивает все квартиры, которые есть в БД ????????????????????????????????????
    def getKvartiras(self):
        try:
            self.__cur.execute(f"SELECT id, adres, image_part, url FROM Kvartiras2 ORDER BY adres")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения квартир из БД"+str(e))
        
        return[]

##Метод добавления новой квартиры (от лица арендодатор) ???????????????
    def newKvartira(self, adres, cena, rooms, SobstvenikId):
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM Kvartira WHERE adres LIKE ?")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Такая квартира уже существует")
                return False
            self.__cur.execute("INSERT INTO Kvartira (adres, cena, rooms, SobstvenikId) VALUES(NULL, ?, ?, ?, ?)", (adres, cena, rooms, SobstvenikId))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления квартиры в Базу Данных" +str(e))
            return False
        return True
    
    def getKvartiraByUrl(self, url):
        try:
            self.__cur.execute("SELECT Kvartiras2.adres, Kvartiras2.image_part, Kvartira.cena, Kvartira.rooms FROM Kvartiras2 LEFT JOIN Kvartira ON Kvartiras2.KvartiraId = Kvartira.id WHERE Kvartiras2.url = ?", (url,))
            return self.__cur.fetchone()
        except sqlite3.Error as e:
            print("Ошибка получения квартиры" + str(e))
        return None

    def newZayavka(self, zhelaemyi_adres, zhelaemyi_cena, zhelaemyi_rooms, user_id=None, status='На рассмотрении', tm=None):
        try:
            if tm is None:
                tm = int(time.time())
            self.__cur.execute(
                "INSERT INTO Zayavka2 (zhelaemyi_adres, zhelaemyi_cena, zhelaemyi_rooms, user_id, status, time) VALUES (?, ?, ?, ?, ?, ?)",
                (zhelaemyi_adres, zhelaemyi_cena, zhelaemyi_rooms, user_id, status, tm))
            self.__db.commit()
            print("Заявка успешно добавлена")
            return True
        except sqlite3.Error as e:
            print("Ошибка добавления заявки в Базу Данных" + str(e))
            print("-" * 50)
            print("КРИТИЧЕСКАЯ ОШИБКА SQLITE:", e)
            print("-" * 50)
            return False

    def getAllZayavki(self):
        try:
            self.__cur.execute("""
                SELECT z.id, z.zhelaemyi_adres, z.zhelaemyi_cena, z.zhelaemyi_rooms,
                       z.status, z.time, z.user_id, u.email
                FROM Zayavka2 z
                LEFT JOIN users u ON z.user_id = u.id
                ORDER BY z.id DESC
            """)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения заявок" + str(e))
        return []

    def updateZayavkaStatus(self, zayavka_id, status):
        try:
            self.__cur.execute("UPDATE Zayavka2 SET status = ? WHERE id = ?", (status, zayavka_id))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print("Ошибка обновления статуса заявки" + str(e))
            return False

    def getZayavkiByUser(self, user_id):
        try:
            self.__cur.execute(
                "SELECT id, zhelaemyi_adres, zhelaemyi_cena, zhelaemyi_rooms, status, time FROM Zayavka2 WHERE user_id = ? ORDER BY id DESC",
                (user_id,))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения заявок пользователя" + str(e))
        return []
        
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute("SELECT COUNT() as count FROM users WHERE email = ?", (email,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким  email уже существует")
                return False
            
            tm = int(time.time())
            self.__cur.execute("INSERT INTO users (name, email, psw, time) VALUES (?, ?, ?, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД" + str(e))
            return False
        
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения даных из БД" + str(e))

        return False

    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            
            return res

        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False