# main.py - Serves REPL from localhost.
from wsgiref.simple_server import make_server
import random

# Config.
PORT = 8080
front = 'index.html'
style = 'style.css'


def main ():
    print "Serving {} on localhost:{}...".format (front, PORT)
    serve()

def repl_serv (environ, start_response):
    if style in environ['PATH_INFO']:
        start_response ('200 OK', [('Content-type', 'text/css')])
        with open (style, 'r') as f:
            css = f.read()
            return css
    start_response ('200 OK', [('Content-type', 'text/html')])
    request = environ ['REQUEST_METHOD'].upper().strip()
    print request
    if request == "POST":
        length = int(environ['CONTENT_LENGTH'])
        msg = environ['wsgi.input'].read (length)
        #return ''.join(random.sample(msg, len(msg)))
        r = str (len (msg))
        if 'foo' in msg:
            return """
            <font color="red">FOO</font>
            """.strip()
        return r
    with open (front, 'r') as f:
        html = f.read()
        return html

def serve():
    # Create daemon to interact with client.
    httpd = make_server ('', PORT, repl_serv)
    httpd.serve_forever()


if __name__ == '__main__':
    main()

