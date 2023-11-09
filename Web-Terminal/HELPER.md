> # Adding users to database manually

```py
@app.route("/null", methods=["GET", "POST"])
def null():
    # Create some users <-- delete this after
    print("Adding sample users to database...")
    hashed_password = bcrypt.generate_password_hash("master").decode('utf-8')
    user1 = User(username="master", password=hashed_password)
    hashed_password = bcrypt.generate_password_hash("wellick123").decode('utf-8')
    user2 = User(username='tyrell', password=hashed_password)
    hashed_password = bcrypt.generate_password_hash("r0b0t").decode('utf-8')
    user3 = User(username='sams3pi0l', password=hashed_password)

    # Add users to the database session
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    # Commit the changes to the database
    db.session.commit()

    print("Done, checkout the database now.")
    return redirect(url_for("login"))
```