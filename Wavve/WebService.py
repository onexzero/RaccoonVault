import sys
import os
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import WavveIptvHelper as WavveUtil

class MyHTTPRequestHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        if '?' in self.path:
            result = urlparse(self.path)
            params = parse_qs(result.query)
            try:
                _user = params["user"][0]
                _pass = params["pass"][0]
                _target = params["what"][0].lower()
                print(_user,_pass,_target)
            except Exception as e:
                print(str(e))
                self.send_error(403)
            else:
                credential = WavveUtil.doLogin(_user,_pass)
                if credential != None :
                    if _target == 'epg':
                        file = "wavve.xml"
                        if not os.path.exists(file):
                            if WavveUtil.createEPG(credential,"wavve.xml"):
                                print('EPG created!\n')
                            else:
                                print('EPG creation failed!\n')
                                file = None
                    elif 'm3u':
                        file = "wavve.m3u"
                        if not os.path.exists(file):
                            if not os.path.exists(file) and WavveUtil.createM3U(credential,"wavve.m3u"):
                                print('M3U created!\n')
                            else:
                                print('M3U creation failed!\n')
                                file = None
                    else:
                        print("Invalid argument - " + _target)

                    WavveUtil.doLogout(credential)

                    if file != None:
                        with open(file, 'rb') as f:
                            self.send_response(200)
                            self.send_header( 'Content-type', 'text/html; charset=utf-8' )
                            fs = os.fstat(f.fileno())
                            self.send_header("Content-Length", str(fs.st_size))
                            self.end_headers()
                            shutil.copyfileobj(f, self.wfile)
                    else:
                        self.send_error(500)

        self.send_error(403)

    def do_POST(self):
        self.send_error(403)

#자바에서 public static void main() 메소드와 같다.
if __name__ == '__main__':
    httpd = HTTPServer( ('192.168.0.51', 7070), MyHTTPRequestHandler )
    print( 'Server Start' )
    httpd.serve_forever()
    print( 'Server End' )