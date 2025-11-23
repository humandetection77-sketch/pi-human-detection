from gpiozero import LED
from http.server import BaseHTTPRequestHandler, HTTPServer

LED_PIN = 18
led = LED(LED_PIN)  # gpiozero handles SOC access correctly on Pi 5

class LEDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/on":
            led.on()
            self.respond(b"LED ON")
        elif self.path == "/off":
            led.off()
            self.respond(b"LED OFF")
        else:
            self.respond(b"Unknown command")

    def respond(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(msg)

server = HTTPServer(("0.0.0.0", 8080), LEDHandler)
print("LED server running on port 8080...")
server.serve_forever()
