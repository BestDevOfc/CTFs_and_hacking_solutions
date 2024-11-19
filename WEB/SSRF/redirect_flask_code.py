from flask import Flask, redirect, request

app = Flask(__name__)

@app.route("/")
def handle_request():
    # Log the initial request details (optional)
    print(f"Request from: {request.remote_addr}")
    
    # Redirect the requester to another URL (or back to the same endpoint)
    return redirect("http://challenge.localhost", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
