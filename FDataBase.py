import sqlite3

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

    def newZayavka(self, zhelaemyi_adres, zhelaemyi_cena, zhelaemyi_rooms):
        try:
            self.__cur.execute("INSERT INTO Zayavka2 (zhelaemyi_adres, zhelaemyi_cena, zhelaemyi_rooms) VALUES (?, ?, ?)", (zhelaemyi_adres, zhelaemyi_cena,zhelaemyi_rooms))
            self.__db.commit()
            print("Заявка успешно добавлена")
            return True
        except sqlite3.Error as e:
            print("Ошибка добавления заявки в Базу Данных" +str(e))
            print("-" * 50)
            print("КРИТИЧЕСКАЯ ОШИБКА SQLITE:", e)
            print("-" * 50)
            return False