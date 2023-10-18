from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def handle_commands():
    routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
    command = request.form["command"]
    args = command.split()
    cmd = args[0]

    match(cmd):
        case "cd":
            route = args[1]
            if route in routes:
                return redirect(url_for(route))
        case "home":
            print("Redirecting to home...")
            return redirect(url_for("root"))
        case _:
            pass

@app.route("/ls", methods=["GET"])
def list_folders():
    return render_template("information/list_folders.html")

@app.route("/help", methods=["GET"])
def help():
    return render_template("information/help.html")

@app.route("/whois", methods=["GET"])
def whois():
    return render_template("information/whois.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
        command = request.form["command"]
        args = command.split()
        cmd = args[0]

        match(cmd):
            case "cd":
                route = args[1]
                if route in routes:
                    return redirect(url_for(route))
            case "home":
                print("Redirecting to home...")
                return redirect(url_for("root"))
            case _:
                pass
    
    return render_template("about.html")

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        routes = [r.endpoint for r in app.url_map.iter_rules() if r.endpoint != 'static']
        command = request.form["command"]
        args = command.split()
        cmd = args[0]

        match(cmd):
            case "cd":
                route = args[1]
                if route in routes:
                    return redirect(url_for(route))
            case "home":
                print("Redirecting to home...")
                return redirect(url_for("root"))
            case _:
                pass
    return render_template("root.html")

if  __name__ == "__main__":
    app.run(debug=True)
