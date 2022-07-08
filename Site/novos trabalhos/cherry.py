from stringprep import in_table_c21_c22
import cherrypy
import sqlite3 as sql
import sys
import os
import json
import html
from PIL import Image
from html.parser import HTMLParser
from PIL import ExifTags
cherrypy.config.update({'server.socket_port': 10008,})

PATH = os.path.abspath(os.path.dirname(__file__))
conf = {"/":
        {
            "tools.staticdir.root": PATH
        },
        "/assets/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/css")        
        },
        "/assets/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/js")        
        },
        "/assets/imgs": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/imgs")        
        },
        "/assets/vendors/themify-icons/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/vendors/themify-icons/css")        
        },
        "/assets/vendors/owl-carousel/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/vendors/owl-carousel/css")        
        },
        "/assets/vendors/jquery": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/vendors/jquery")        
        },
        "/assets/vendors/bootstrap": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/vendors/bootstrap")        
        },
        "/assets/vendors/owl-carousel/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "assets/vendors/owl-carousel/js")        
        },
        "/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "js")        
       
		 },
        "/img": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "img")  
            },
        "/ima": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(PATH, "ima")       
       
		}
}
users = {}
show = {}

def databasecreate(db):
    db = sql.connect("database/database.db")
    c = db.cursor()
    c.execute("""CREATE TABLE pic(nome TEXT, pass TEXT, pic TEXT)""")
    db.commit()
    db.close()
    


    
    return None



def  create(user, pas):
    db = sql.connect("database/database.db")
    c = db.cursor()
    print(user)
    print(pas)
    c.execute("INSERT INTO pic VALUES (?, ?, ?)", (user, pas, ""))
    db.commit()
    rows =  c.execute("SELECT * FROM pic")

    for row in rows:
        print(row)
    
    db.close()
    a = {"id" : user, "pass" : pas}
    users.update(a)
    
    

  
    
    return None

def  inis(user, pas):
    db = sql.connect("database/database.db")
    c = db.cursor()
    a = c.execute("SELECT nome, pass FROM pic WHERE pass LIKE ? AND nome LIKE ?", (pas, user))
    b = ""
    for row in a:
        a = row[0]
        b = row[1]
                
    print(a)
    print(b)
    db.close()
    if((a != user) or (b != pas)):
            return False
    else:
            a = {"id" : user, "pass" : pas}
            users.update(a)
            return True
            
    
    
    
    

  
    


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
        im1.save("img/"+i1.filename)
        im1.close()
        im2.close()
        db = sql.connect("database/database.db")
        c = db.cursor()
        print(type(i1.filename))
        print(i1.filename)
        c.execute("INSERT INTO pic VALUES (?, ?, ?)", ( users["id"], users["pass"], str(i1.filename)))
        b = c.execute("SELECT * FROM pic")
        for row in b:
            print(row)
        db.commit()
        db.close()
        return None

def pics():
    p = 0
    a = []
    db = sql.connect("database/database.db")
    c = db.cursor()
    b = c.execute("SELECT * FROM pic")
    for row in b:
        if((row[0] == show["id"])):
            if(row[2] != ''):
                a.append(row[2])
                p = p+1
            
    db.close()


    
    i = 0
    while(i<p):
        cherrypy.response.headers["Content-Type"] = "application/json"
        print(a[i])
        return json.dumps({"pics": a[i]})

def sendinfo():
    p = 0
    a = []
    e = []
    db = sql.connect("database/database.db")
    c = db.cursor()
    b = c.execute("SELECT * FROM pic")
    for row in b:
        d = 0;
        if((row[0] != users["id"]) and (row[1] != users["pass"])):
            if(row[2] != ''):
                if(len(a) == 0):
                            e.append(row[2])
                            d = d+1
                
                            a.append(row[0])
                            p = p+1
                else:
                    i = 0
                    print(len(a))
                    while((d == 0) and (i<(len(a)))):
                        print(i)
                        if((row[0] != a[i]) and (row[2] != e[i])):
                            e.append(row[2])
                            d = d+1
                
                            a.append(row[0])
                            p = p+1
                            
                        i = i+1
    db.close()
    i = 0
    print(p)
    while(i<p):
        i = i+1
        cherrypy.response.headers["Content-Type"] = "application/json"
        print(a[i])
        print(e[i])
        return json.dumps({"u": a[i], "pic": e[i]})


class us(object):
    @cherrypy.expose
    def index(self):
        return None
    @cherrypy.expose
    def usepic(self):
        return open("html/showpic.html")
    @cherrypy.expose
    def showpic(self):
        print("ola")
        cherrypy.response.headers["Content-Type"] = "application/json"
        return pics().encode("utf-8", "ignore")
    @cherrypy.expose
    def show(self, user):
        print("ola")
        a = {"id" : user}
        show.update(a)
        return None
   
    
class log(object):
    @cherrypy.expose
    def index(self):
        return open("html/sign.html")
    @cherrypy.expose
    def inerr(self):
        return open("html/logE.html")
    @cherrypy.expose
    def cre(self, user, pas):
        create(user, pas)
        return None
    @cherrypy.expose
    def log2(self, user, pas):
        d = inis(user, pas)
        if (d == True):
            print("done")
            print(users["id"])
            a = "done"
            a = {"r" : "done"}
            return None
        else:
            print("1")
            return None
    @cherrypy.expose
    def log3(self):
        print("d")
        d = {}
        s = json.dumps({"r": "nop"})
        for i in users:
            if(i == ''):
                print("d")
                s = json.dumps({"r": "nop"})
            else:
                print("d")
                s = json.dumps({"r": "done"})
        
        cherrypy.response.headers["Content-Type"] = "application/json"
        return s.encode("utf-8", "ignore")
    @cherrypy.expose
    def logoff(self):
        users.pop("id")
        users.pop("pass")
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
        self.us = us()
    
    @cherrypy.expose
    def index(self):
        db = sql.connect("database/database.db")
        c = db.cursor()
        try:
            a = c.execute("SELECT * FROM pic")
            print(9)
            for row in a:
                print(row)
            db.close()
        except(sql.Error):
            databasecreate(db)
            print(0)
            db.close()
          
        
            
        return open("html/LogIndex.html")
        
    @cherrypy.expose
    def rot(self):        
        return open("index.html")
    @cherrypy.expose
    def showim(self):        
        return sendinfo().encode("utf-8", "ignore")
    
if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 10017})
    cherrypy.quickstart(Root(), "/",config = conf)
    
