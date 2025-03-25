from api import *

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)