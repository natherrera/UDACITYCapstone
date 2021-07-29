from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db_path = "postgres://cvjivdnclvyjog:51ec8c20289b6e35d453eaab45da55b45d17787a20d3748679c5394b25a4fb9c@ec2-34-233-114-40.compute-1.amazonaws.com:5432/dechcibns75qiv"
db = SQLAlchemy()


def setup_db(app, database_path=db_path):
    app.config.from_object('config')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app,db)
    with app.app_context():
      db.create_all()

    # add one demo row which is helping in POSTMAN test

# ROUTES
class Actor(db.Model):
    __tablename__ = 'Actor'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(50), nullable=False)

    def __repr__(self):
        return f'< Actor {self.id} {self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'gender': self.gender
        }

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = Column(Integer(), primary_key=True)
    title = Column(String(80), nullable=False)
    release_date = Column(String(80), nullable=False)
    
    def __repr__(self):
        return f'< Movie {self.id} {self.title}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
