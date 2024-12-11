from flask import Flask
from threading import Thread

# สร้างแอป Flask
app = Flask(__name__)

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    # รันเซิร์ฟเวอร์ Flask
    app.run(host="0.0.0.0", port=8080, debug=False)

def keep_alive():
    # เริ่มเซิร์ฟเวอร์ในเธรดใหม่
    server = Thread(target=run, daemon=True)
    server.start()
