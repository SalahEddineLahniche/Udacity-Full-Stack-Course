from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm.exc import NoResultFound

import re

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/restaurants":
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello ! this is resto, your website for restaurants.</h1>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<span>%s</span>&ensp;<a href='restaurant/%d/edit'>edit</a> - <a href='restaurant/%d/delete'>delete</a><br>" % (restaurant.name, restaurant.id, restaurant.id)
                output += "<br><a href='restaurant/new'>Add new</a>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
            m = re.match(r"/restaurant/(?P<id>\d*)/edit", self.path)
            if m:
                restaurant_id = (int)(m.group("id"))
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello ! this is resto, your website for restaurants.</h1>"
                output += "<h3>Updating a restaurant</h3>"

                try:
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    output += "<form method='post' enctype='multipart/form-data' action=''><input name='name' type='text' value='%s'><input type='submit' value='Submit'></form>" % (restaurant.name)

                except NoResultFound:
                    output += "<p style='color: red;'>restaurant \"%d\" not found</p>" % restaurant_id


                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            m = re.match(r"/restaurant/(?P<id>\d*)/delete", self.path)
            if m:
                restaurant_id = (int)(m.group("id"))
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello ! this is resto, your website for restaurants.</h1>"
                try:
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    output += "<h3>Do you really want to delete %s ?</h3>" % restaurant.name
                    output += "<form method='post' enctype='multipart/form-data' action=''><input type='submit' value='Yes'><button onclick='window.history.back();'>Go back</button></form>"

                except NoResultFound:
                    output += "<p style='color: red;'>restaurant \"%d\" not found</p>" % restaurant_id


                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path == "/restaurant/new":
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello ! this is resto, your website for restaurants.</h1>"
                output += "<h3>Adding new restaurant</h3>"
                output += "<form method='post' enctype='multipart/form-data' action=''><input name='name' type='text'><input type='submit' value='Add'></form>"


                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
                
        except Exception as e:
            print e.message

    def do_POST(self):
        try:
            if self.path == "/restaurant/new":
                self.send_response(301)
                self.send_header('content-type', 'text/html')

                output = ""
                output += "<html><body>"
                output += "<h1>Hello ! this is resto, your website for restaurants.</h1>"

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get("name")

                try:
                    restaurant = Restaurant(name=restaurant_name[0])
                    session.add(restaurant)
                    session.commit()
                    output += "<p>Restaurant has been added successfully !</p><a href='../../restaurants'>Go home</a>"
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
                except Exception as e:
                    print e.message
                    output += "<p style='color: red;'>An error has been occured while adding the restaurant</p>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            m = re.match(r"/restaurant/(?P<id>\d*)/edit", self.path)
            if m:
                restaurant_id = (int)(m.group("id"))
                self.send_response(301)
                self.send_header('content-type', 'text/html')

                output = ""
                output = ""
                output += "<html><body>"
                output += "<h1>Hello ! this is resto, your website for restaurants.</h1>"

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get("name")

                try:
                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                    restaurant.name = restaurant_name[0]
                    session.add(restaurant)
                    session.commit()
                    output += "<p>Restaurant has been updated successfully !</p><a href='../../../restaurants'>Go home</a>"
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
                except NoResultFound:
                    output += "<p style='color: red;'>The request restaurant is not found</p>"
                except Exception:
                    output += "<p style='color: red;'>An error has occured while updating this restaurant</p>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            m = re.match(r"/restaurant/(?P<id>\d*)/delete", self.path)
            if m:
                restaurant_id = (int)(m.group("id"))
                self.send_response(301)
                self.send_header('content-type', 'text/html')

                output = ""
                output = ""
                output += "<html><body>"
                output += "<h1>Hello ! this is resto, your website for restaurants.</h1>"

                try:
                    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                    session.delete(restaurant)
                    session.commit()
                    output += "<p>Restaurant has been deleted successfully !</p><a href='../../../restaurants'>Go home</a>"
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
                except NoResultFound:
                    output += "<p style='color: red;'>The request restaurant is not found</p>"
                except Exception:
                    output += "<p style='color: red;'>An error has occured while deleting this restaurant</p>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


        except Exception as e:
            print e.message

def main():
    try:
        port = 8080
        webserver = HTTPServer(('', port), webserverHandler)
        print "webserver running on port %d" % port
        webserver.serve_forever()


    except KeyboardInterrupt:
        print "Closing connection ..."
        webserver.socket.close()
        pass

if __name__ == "__main__":
    main()
