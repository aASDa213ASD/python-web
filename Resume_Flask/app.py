from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/ls", methods=["GET"])
def list_folders():
    return render_template("information/list_folders.html")

@app.route("/help", methods=["GET"])
def help():
    return render_template("information/help.html")

@app.route("/whois", methods=["GET"])
def whois():
    return render_template("information/whois.html")

@app.route("/projects", methods=["GET"])
def projects():
    return render_template("information/projects.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
        command = request.form["command"]
        args = command.split()
        cmd = args[0]

        match(cmd):
            case "cd":
                route = None
                try:
                    route = args[1]
                except Exception:
                    pass
                if route and route in routes:
                    return redirect(url_for(route))
                elif not route or route == "/":
                    print("redirecting to root")
                    return redirect(url_for("root"))
            case _:
                pass
    return render_template("about.html")

@app.route("/gamehacking", methods=["GET", "POST"])
def gamehacking():
    if request.method == "POST":
        routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
        command = request.form["command"]
        args = command.split()
        cmd = args[0]

        match(cmd):
            case "cd":
                route = None
                try:
                    route = args[1]
                except Exception:
                    pass
                if route and route in routes:
                    return redirect(url_for(route))
                elif not route or route == "/":
                    print("redirecting to root")
                    return redirect(url_for("root"))
            case _:
                pass
    return render_template("gamehacking.html")

@app.route("/gallery", methods=["GET", "POST"])
def gallery():
    if request.method == "POST":
        routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
        command = request.form["command"]
        args = command.split()
        cmd = args[0]

        match(cmd):
            case "cd":
                route = None
                try:
                    route = args[1]
                except Exception:
                    pass
                if route and route in routes:
                    return redirect(url_for(route))
                elif not route or route == "/":
                    print("redirecting to root")
                    return redirect(url_for("root"))
            case _:
                pass
    return render_template("gallery.html")

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
        print(f"Available Routes Internal: {routes}")
        command = request.form["command"]
        args = command.split()
        cmd = args[0]

        match(cmd):
            case "cd":
                route = None
                try:
                    route = args[1]
                except Exception:
                    pass
                if route and route in routes:
                    return redirect(url_for(route))
                elif not route or route == "/":
                    print("redirecting to root")
                    return redirect(url_for("root"))
            case _:
                pass
    return render_template("root.html")

if  __name__ == "__main__":
    app.run(debug=True)
