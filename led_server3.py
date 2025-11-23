from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO

LED_PIN = 18  # GPIO18

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

class LEDHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/on":
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED ON")
            self.respond(b"LED ON")
        elif self.path == "/off":
            GPIO.output(LED_PIN, GPIO.LOW)
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
    GPIO.cleanup()
