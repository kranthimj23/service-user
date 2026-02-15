
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/ready')
def ready9():
    return jsonify({"status": "ready"})

@app.route('/write')
def write():
    print("write function being executed")
    print("Hare Rama")
    return jsonify({"msg": "Data1 written to service-user"})

#this is app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
