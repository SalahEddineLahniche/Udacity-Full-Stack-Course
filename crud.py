#Preconfig for sessions managing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

#adding an entery - CREATE
myFirstRestaurant = Restaurant(name = "TACOS")
session.add(myFirstRestaurant)
session.commit()


items = session.query(Restaurant).all()
for item in items:
    print item.name