# main.py - Serves REPL from localhost.
from wsgiref.simple_server import make_server
import random
from code import InteractiveInterpreter as II
import os
import sys
import StringIO

# Config.
PORT = 8080
front = 'index.html'
style = 'style.css'
interp = II ()
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
        if "--python" in sys.argv:
            # Parse Python
            s = sys.stdout
            output = StringIO.StringIO ()
            sys.stdout = output
            interp.runsource (msg)
            sys.stdout = s
            out = output.getvalue().replace ('\n', '<br>')
            return out
        return os.popen (msg).read().replace ('\n', '<br>')

    with open (front, 'r') as f:
        html = f.read()
        return html

def serve():
    # Create daemon to interact with client.
    httpd = make_server ('', PORT, repl_serv)
    httpd.serve_forever()


if __name__ == '__main__':
    main()

