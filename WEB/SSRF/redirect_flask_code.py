from flask import Flask, redirect, request

app = Flask(__name__)

@app.route("/")
def handle_request():
    return redirect("file:///etc/passwd", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969, debug=True)
