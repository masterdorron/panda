from flask import Flask
app = Flask(__name__)

@app.route('/api', methods=['GET'])
def hello():
    return {"message": "Test task for Panda Team!"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)