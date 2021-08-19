import time
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer

redis_db = redis.StrictRedis(host='redis', port=6379)
hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        retries = 5
        while True:
            try:
                average_word_len = redis_db.get("book.average_word_len")
                ratio_vowel = redis_db.get("book.ratio_vowel")
                occurrences_of_boat_derivatives = redis_db.get("book.occurrences_of_boat_derivatives")
                occurrences_of_boat = redis_db.get("book.occurrences_of_boat")

            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title></title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<table border=1><tr><td>" + average_word_len + "</td><td>" + ratio_vowel + "</td><td>" + occurrences_of_boat_derivatives + "</td><td>" + occurrences_of_boat + "</td></tr></table>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

