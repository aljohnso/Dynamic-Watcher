from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class CalenderData(db.Model):
    __tablename__ = "CalenderData"
    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(120))
    userName = db.Column(db.String(120))
    userCalenderBlob = db.Column(db.String(5000))

    def __init__(self, blob=None):
        print(blob)
        self.userEmail = str(list(blob)[0]['organizer']['email'])
        self.userName = str(list(blob)[0]['organizer']['displayName'])
        self.userCalenderBlob = str(blob)#TODO: This breaks things


    @property
    def serializeTable(self):
        """ Return object data in easily serializeable format
            https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask?noredirect=1&lq=1
        """
        return {
            'id': self.id,
            # Lol this is a total hack but it works so whatever
            'userName': self.Name
            }