from flask import Flask, request, redirect, render_template, flash, url_for
import shelve
import os


app = Flask(__name__, static_url_path="/static")
app.secret_key = "parangarigotirrimuruano" # Add this! Change it to your own random string.


'''with shelve.open("user_data.shelf") as db:#   
    db["kelvin"] = {"password": "1"}
    db["xisto"] = {"password": "xisto"}
    db["mae"] = {"password": "mae"}
    db["tia"] = {"password": "cida"}
    db["jean"] = {"password": "jebz"}
    db["taigo"] = {"password": "taigo"}
'''
#debug shelve
# --- TEMPORARY DIAGNOSTIC ---
with shelve.open("user_data.shelf") as db_check:
    print("Checking shelf content after potential update:")
    for key in db_check:
        print(f"User: {key}, Data: {db_check[key]}")
# --- END TEMPORARY DIAGNOSTIC ---



@app.route("/login", methods=["POST"])
def login():
    form = request.form
    try:
        with shelve.open("user_data.shelf") as db: # Open the database/key
            if db[form["username"]]["password"] == form["password"]:
                return redirect("/yup") # Redirect to a success page/GIF
            else:
                return redirect("/nope") # Redirect to a failure page/GIF
    except KeyError: # If username doesn't exist
        return redirect("/nope")                                                                     

@app.route("/nope")
def nope():
    # In the original, this showed a GIF. For now, just text is fine.
     return "<img src='static/fallouterror.gif'>\n usuario ou senha incorretos"
 #   return "Login failed, you robot!"

@app.route("/yup")
def yup():
    return render_template("change.html") # Assumes change.html is in 'templates'


@app.route("/change", methods=["POST"])
def change():
    form = request.form
    username = form["username"]
    new_password = form["npassword"]  # Make sure this matches your form input name

    with shelve.open("user_data.shelf") as db:
        if username in db:
            user_data = db[username]
            user_data["password"] = new_password
            db[username] = user_data  # Save updated dict back to shelf
 # Flash a success message before redirecting
            flash(f"Senha alterada para o usuário '{username}' com sucesso!", "success") # "success" is a category
        else:
            # Flash an error message
            flash(f"Usuário '{username}' não encontrado.", "error") # "error" is a category
    
    return redirect(url_for('index')) # Redirect to the homepage (your '/' route)

@app.route("/")
def index():
    # This loads your login.html page
    page = ""
    try:
      return render_template("login.html") # Assumes change.html is in 'templates'
    except FileNotFoundError:
        return "login.html not found!"
    return page
# This is the standard Python way to check if the script is being run directly
# If it is, then it starts the Flask development server
# --- Standard Run Settings ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable
    app.run(host="0.0.0.0", port=port)  # Listen on 0.0.0.0 and use the specified port

  # You can change 81 to 5000 if you prefer, or remove host and port arguments entirely.
    