from settings import db, pwd_context


class User(db.Model):
    __bind_key__ = 'user'
    __tablename__ = 'api_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __repr__(self):
        return f'<User: {self.username}>'

    def verifyPassword(self, password):
        return pwd_context.verify(password, self.password)

    @staticmethod
    def to_json(data):
        return {
            "id": data.id,
            "username": data.username,
            "password": data.password
        }

