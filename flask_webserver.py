from flask import Flask, url_for, redirect, request, render_template, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm.exc import NoResultFound

import re

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
def ShowRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('show_restaurants.html', restaurants=restaurants)

@app.route('/JSON/')
def ShowRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurant/new', methods=["POST", "GET"])
def AddRestaurant():
    if request.method == "GET":
        return render_template('add_restaurant.html')
    if request.method == "POST":
        try:
            restaurant_name = request.form['name']
            restaurant = Restaurant(name=restaurant_name)
            session.add(restaurant)
            session.commit()
            return redirect('/')
        except Exception as e:
            return render_template('error.html', error=e.message)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['POST', 'GET'])
def DeleteRestaurant(restaurant_id):
    if request.method == "GET":
        try:
            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
            return render_template('delete_restaurant.html', restaurant=restaurant.name)
        except Exception as e:
            return render_template('error.html', error=e.message)
    if request.method == "POST":
        try:
            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
            session.delete(restaurant)
            session.commit()
            return redirect('/')
        except Exception as e:
            return render_template('error.html', error=e.message)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['POST', "GET"])
def EditRestaurant(restaurant_id):
    if request.method == "GET":
        try:
            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
            return render_template('edit_restaurant.html', name=restaurant.name)
        except Exception as e:
            return render_template('error.html', error=e.message)
    if request.method == "POST":
        try:
            restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()
            return redirect('/')
        except Exception as e:
            return render_template('error.html', error=e.message)


@app.route('/restaurant/<int:restaurant_id>/')
def ShowMenu(restaurant_id):
    output = ""
    output += "<html><body>"
    output += "<h1>Welcome to &#161;Resto the first restaurants guide in max-red-desktop.</h1>"
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        output += "<h2>Restaurant: %s</h2>" % restaurant.name
        output += "<ul>"
        menus = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        for menu in menus:
            output += "<li>%s-<em>%s</em>&ensp;-&ensp;%s</li>" % (menu.name, menu.description, menu.price)
        output += "</ul>"
    except NoResultFound:
        output += "<p style='color:red;'>Restaurant not found<p><button onclick='window.history.back()'>Go back</button>"
    output += "</body></html>"
    return output



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)

