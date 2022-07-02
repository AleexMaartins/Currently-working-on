from stringprep import in_table_c21_c22
import cherrypy
import sqlite3 as sql
import sys
import os
import json
from PIL import Image
from PIL import ExifTags
cherrypy.config.update({'server.socket_port': 10008,})

PATH = os.path.abspath(os.path.dirname(__file__))
conf = {"/":
        {
            "tools.staticdir.root": PATH
        },
        "/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "css")        
        },
        "/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "js")        
       
		 },
        "/img": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "img")        
       
		}
}
def databasecreate(db):
    db.execute("CREATE TABLE pic(nome TEXT, pass TEXT, pic TEXT)")

    
    return None

def upload(i1, i2):
        im1 = Image.open("uploads/" +i1.filename)
        im2 = Image.open("uploads/" +i2.filename)
        x, y = im1.size
        p1 = im1.getpixel( (0+x/4, 0+y/4) )
        x, y = im2.size
        p2 = im2.getpixel( (0, 0) )
        width, height = im1.size
        for x in range(width):
            for y in range(height):
                if(p2[3] == 0):
                    continue

                r = int(p1[0]*(1-0.5)+p2[0]*0.5)
                g = int(p1[1]*(1-0.5)+p2[1]*0.5)
                b = int(p1[2]*(1-0.5)+p2[2]*0.5)

        cherrypy.response.headers["Content-Type"] = "json"
        im1.save("img/Result.jpg")
        im1.close()
        im2.close()
        return None

class log(object):
    @cherrypy.expose
    def index(self):
        return None

class image(object):
    
    @cherrypy.expose
    def index(self):
        return open("html/image.html")
    @cherrypy.expose
    def done(self, i1, i2):
        print("done")
        fo = open("uploads/" + i1.filename, "wb")
        while True:
            data = i1.file.read(8192)
            if not data: break
            fo.write(data)
        fo.close()

        print("done")
        fo = open("uploads/" + i2.filename, "wb")
        while True:
            data = i2.file.read(8192)
            if not data: break
            fo.write(data)
        fo.close()
        print("done")
        upload(i1, i2)
        print("done")
        return print("done")

    
    
       

class Root:
    
    def __init__(self):
        self.image = image()
        self.log = log()
        
    @cherrypy.expose
    def index(self):
        db = sql.connect("database/database.db")
        try:
            db.execute("SELECT * FROM pic")
        except(db.DatabaseError):
            databasecreate(db)
            
        
            
        return open("html/index.html")
if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 10017})
    cherrypy.quickstart(Root(), "/",config = conf)
