import socket
import os
import gzip  # for gzip compression
import webbrowser  # for testing: open webbrowser after start


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket vorbereiten
c.bind(('localhost', 8080))  # an Port 8080 binden
c.listen(5)  # auf hereinkommende Verbindungen lauschen

# for testing: immediately open browser
# webbrowser.open_new_tab("http://localhost:8080/index.html")

while 1:
    csock, caddr = c.accept()
    conn = csock.makefile(mode='rwb', buffering=1)

    def w(txt):
        """Decode as UTF-8 and write to client connection"""
        conn.write(bytes(txt, 'UTF-8'))

    # Aufgabe 1: Function to encapsulate calculation of Content-Length and sending body
    def send_body(body):
        w("Content-Length: {}\n\n".format(len(body)))  # we need two \n !
        conn.write(body)

    # Aufgabe 2: Send file index for static directory
    def send_index():
        w("HTTP/1.1 200 OK\n")  # nasty code duplication. don't do this at home!
        import datetime
        w("Date: %s\n" % datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"))
        w("Content-Type: text/plain\n")  # we have plain text
        w("\n")
        for f in os.listdir('./static'):
            w("%s\n" % f)  # one file per line

    # Read request
    while 1:
        request_line = conn.readline().decode('utf-8').strip()
        if request_line.strip():
            break
    method, resource, protocol = request_line.split(" ")
    print("Request: %s %s %s" % (method, resource, protocol))
    while True:
        header_line = conn.readline().decode('utf-8').strip()
        if not header_line:
            break
        (headerfield, headervalue) = header_line.split(":", 1)

        # Aufgabe 1: Add handling of Accept-Encoding header

        if headerfield == 'Accept-Encoding':  # acceptable compressions

            # split list of acceptable compression algorithms and
            # strip whitespaces from front and back of each of the
            # names.
            #
            # The list comprehension [x.strip() for x in ....] is
            # equivalent to:
            #
            # compressions = []
            # for x in headervalue.split(","):
            #   compressions.append(x.strip())

            compressions = [x.strip() for x in headervalue.split(",")]

    from urllib.parse import unquote
    resource = unquote(resource)
    if ".." in resource: # some protection from directory traversal attacks
        w("HTTP/1.1 500 Internal Server Error\n\n")
        w("500 internal server error.\nDirectory traversal attack attempted.\n")
        conn.close()
        csock.close()
        continue

    if resource == '/':  # Aufgabe 2: file listing for /
        send_index()
    else:  # try to send file
        try:
            f = open('static' + resource, 'rb')
        except IOError:
            w("HTTP/1.1 404 File not found\n\n")
            w("404 File not found: %s\n" % resource)
            print("Response: 404 File not Found")
        else:
            # Write response
            w("HTTP/1.1 200 OK\n")
            import datetime
            w("Date: %s\n" % datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"))

            # guess type from extension
            import mimetypes
            (content_type, encoding) = mimetypes.guess_type(resource)
            if not content_type:
                content_type = "text/plain"
            w("Connection: close\n")
            w("Content-Type: %s\n" % content_type)

            # Aufgabe 1: Add Content-Encoding header if gzip is accepted (we only know gzip)
            if 'gzip' in compressions:
                w("Content-Encoding: gzip\n")

            print("Response: 200 OK, Content-Type: {}".format(content_type))

            # Aufgabe 1: Only difference is whether to apply compression or not
            data = f.read()
            if 'gzip' in compressions:  # apply gzip before sending
                send_body(gzip.compress(data))  # dump whole file compressed
            else:
                send_body(data)  # dump whole file uncompressed

            f.close()

    conn.close()
    csock.close()

