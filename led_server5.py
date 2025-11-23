from gpiozero import LED, Device
from gpiozero.pins.lgpio import LGPIOFactory
from http.server import BaseHTTPRequestHandler, HTTPServer

# Use LGPIOFactory so gpiozero works on Pi 5 64-bit
Device.pin_factory = LGPIOFactory()

LED_PIN = 18
led = LED(LED_PIN)

class LEDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/on":
            led.on()
            self.respond(b"LED ON")
            print("LED ON")
        elif self.path == "/off":
            led.off()
            self.respond(b"LED OFF")
            print("LED OFF")
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
