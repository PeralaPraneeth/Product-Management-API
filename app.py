from flask import Flask
from extensions import app
from database import database_app

app.register_blueprint(database_app)

if __name__ == "__main__":
    with app.app_context():
        from extensions import db
        db.create_all()
    app.run(debug=True)
