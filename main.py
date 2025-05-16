from flask import Flask, request, redirect, render_template, flash, url_for
import os

app = Flask(__name__, static_url_path="/static")
app.secret_key = "parangarigotirrimuruano"

# --- HARDCODED USER DICTIONARY ---
users = {
    "kelvin": {"password": "1"},
    "xisto": {"password": "xisto"},
    "mae": {"password": "mae"},
    "tia": {"password": "cida"},
    "jean": {"password": "jebz"},
    "taigo": {"password": "taigo"},
    "patrice": {"password": "s2"},
    "neide": {"password": "neide"}
}

@app.route("/login", methods=["POST"])
def login():
    form = request.form
    username = form.get("username")
    password = form.get("password")
    if username in users and users[username]["password"] == password:
        return redirect("/yup")
    else:
        return redirect("/nope")

@app.route("/nope")
def nope():
    return "<img src='/static/fallouterror.gif'>\n usuario ou senha incorretos"

@app.route("/yup")
def yup():
    return render_template("change.html")

@app.route("/change", methods=["POST"])
def change():
    form = request.form
    username = form.get("username")
    new_password = form.get("npassword")
    if username in users:
        users[username]["password"] = new_password
        flash(f"Senha alterada para o usuário '{username}' com sucesso!", "success")
    else:
        flash(f"Usuário '{username}' não encontrado.", "error")
    return redirect(url_for('index'))

@app.route("/")
def index():
    try:
        return render_template("login.html")
    except FileNotFoundError:
        return "login.html not found!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
