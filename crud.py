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

#viewing
items = session.query(MenuItem).all()
for item in items:
    print item.name

#Updating
theVeggieBurger = session.query(MenuItem).filter_by(id = 9).one()
theVeggieBurger.price = "$2.99"
session.add(theVeggieBurger)
session.commit()

#deleting
tacos = session.query(Restaurant).filter_by(name = "TACOS")
for restaurant in tacos:
    session.delete(restaurant)
    session.commit()