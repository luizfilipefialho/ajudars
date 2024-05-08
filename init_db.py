from app import app, db  # Import the app and db directly

with app.app_context():
    db.create_all()  # This will create all tables
