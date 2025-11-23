from http.server import BaseHTTPRequestHandler, HTTPServer
from gpiozero import LED

LED_PIN = 18
led = LED(LED_PIN)

class LEDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/on":
            led.on()
            print("LED ON")
            self.respond(b"LED ON")
        elif self.path == "/off":
            led.off()
            print("LED OFF")
            self.respond(b"LED OFF")
        else:
            self.respond(b"Unknown command")

    def respond(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(msg)

try:
    server = HTTPServer(("0.0.0.0", 8080), LEDHandler)
    print("LED server running on port 8080...")
    server.serve_forever()
finally:
    led.off()
