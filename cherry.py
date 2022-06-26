#cv
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

def upload( f1, f2):
        im1 = Image.open(f1)
        im2 = Image.open(f2)
        p1 = im1.getpixel( (x+0, y+0) )
        p2 = im2.getpixel( (x,y) )
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
        return json.dumps()

class image(object):
    
    @cherrypy.expose
    def index(self):
        return open("html/image.html")
    @cherrypy.expose
    def done(self, myFile):
        fo = open("uploads/" + myFile.filename, "wb")
        while True:
            data = myFile.file.read(8192)
            if not data: break
        fo.write(data)
        fo.close()
        print("done")
        return None

    
    
       

class Root:
    
    def __init__(self):
        self.image = image()
        
    @cherrypy.expose
    def index(self):
        return open("html/index.html")
if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 10017})
    cherrypy.quickstart(Root(), "/",config = conf)
