from .database import SessionLocal, engine

class DB:

    db = None 

    def __init__(self):
        print("Init shared db")

    def init_db(self):
        self.db = SessionLocal()
        print("I am instance {0}".format(self))
        try:
            # yield'ın kalması mantıklı mı
            yield self.db
        finally:
            self.db.close()

    def get_db(self):
        return self.db