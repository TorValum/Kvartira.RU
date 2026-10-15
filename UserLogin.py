class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        # Проверяем, есть ли в self.__user данные (не равен ли он None)
        return hasattr(self, '_UserLogin__user') and self.__user is not None
    
    def is_active(self):
        return hasattr(self, '_UserLogin__user') and self.__user is not None
    
    def is_anonymous(self):
        # Пользователь считается анонимом, если данных о нём нет
        return not (hasattr(self, '_UserLogin__user') and self.__user is not None)

    def get_id(self):
        return str(self.__user['id'])

    @property
    def name(self):
        return self.__user['name'] if self.__user else None
