https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md


from werkzeug.urls import url_fix # 0.10 to get url_fix()
from secrets import token_urlsafe
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html", error=request.args.get("error"))

@app.route("/new", methods=["POST"])
def create():
    content = request.form.get("content", "")
    if "_" in content or "/" in content:
        return redirect(url_for("index", error="bad_content"))
    if len(content) > 512:
        return redirect(url_for("index", error="long_content", len=len(content)))
    name = f"static/{url_fix(content[:128])}-{token_urlsafe(8)}.html"
    with open(name, "w") as f:
        f.write(content)
    return redirect(name)

'''

*** DID NOT NEED TO URL ENCODE because filename only stores first 128 (could've just put plain ASCII 'A'*128)


..\templates\errors\LMAO2
?error=LMAO2-Nf8C5s1z_4A

..\templates\errors\LMAO(2
/?error=LMAO(2-beWGa51yLsA

..\templates\errors\LMAO{{ 2*2 }}
1) have to DOUBLE URLENCODE the output as well because our browser will
    URL encode and when it's sent to url_fix() it gets URL encoded AGAIN.

..\templates\errors\LMAO{{ 2*2 }}


..\templates\errors\LMAO{{ config.get_items() }}

..\templates\errors\LMAO{{ ()|attr('class') }}


'''

