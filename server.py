#!/usr/bin/env python
import sys
from subprocess import Popen

if sys.version_info[0] < 3:  # python 2
    import BaseHTTPServer
else:  # python 3
    import http.server as BaseHTTPServer

PORT = 7531

if sys.version_info[0] < 3:
    class CompatibilityMixin:
        def send_body(self, msg):
            self.wfile.write(msg+'\n')
            self.wfile.close()
else:
    class CompatibilityMixin:
        def send_body(self, msg):
            self.wfile.write(bytes(msg+'\n', 'utf-8'))


class Handler(BaseHTTPServer.BaseHTTPRequestHandler, CompatibilityMixin):
    def respond(self, code, body=None):
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        if body:
            self.send_body(body)

    def do_GET(self):
        url = self.path.split("?",1)[1].split("=",1)
        print(url)
        if url[0] == "ykdl_url":
            url = url[1]
            if url.startswith('https://www.iqiyi.com/') or url.endswith('.html'):
                pipe = Popen(['ykdl','-p','mpv --merge-files',url])
            else:
                pipe = Popen(['ykdl','-p','mpv', url])
            self.respond(200, "playing...")
        elif url[0] == "mpv_url":
            url = url[1]
            if url.startswith('https:') or url.endswith('.html'):
                pipe = Popen(['mpv',  url])
            else:
                pipe = Popen(['mpv',  url])
            self.respond(200, "casting...")
        elif url[0] == "you-get_url":
            url = url[1]
            if url.startswith('https:') or url.endswith('.html'):
                pipe = Popen(['you-get','-p','mpv',  url])
            else:
                pipe = Popen(['you-get','-p','mpv',  url])
            self.respond(200, "casting...")
        elif url[0] == "annie_url":
            url = url[1]
            if url.startswith('https://www.bilibili.com/') or url.endswith('.html'):
                pipe = Popen(['annie', '-C','-o','C:\迅雷下载','-aria2',  url])
            else:
                pipe = Popen(['annie','-o','C:\迅雷下载','-aria2',  url])
            self.respond(200, "casting...")






def start():
    httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
    print("serving at port {}".format(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" shutting down...")
        httpd.shutdown()


if __name__ == '__main__':
    start()

