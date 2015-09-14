'''
Created on 2014-4-4

@author: 1207263
'''


from http.server import HTTPServer,BaseHTTPRequestHandler
import io,shutil

class MyHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print ("It's GET" ) 
        r_str="Hello World"
        enc="UTF-8"
        encoded = ''.join(r_str).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        shutil.copyfileobj(f,self.wfile)
    def do_POST(self):  
        print ("It's POST" ) 
        print (self.headers)
        s=self.rfile.read1(2046)
        print(s)
        print(s.decode('GBK'))
        r_str="Hello World"
        enc="UTF-8"
        encoded = ''.join(r_str).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)  
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        shutil.copyfileobj(f,self.wfile)

httpd=HTTPServer(('',8080),MyHttpHandler)
print("Server started on 127.0.0.1,port 8080.....")
httpd.serve_forever()