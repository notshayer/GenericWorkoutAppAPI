from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from core import *
import datetime

# Register new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400

    # Hash the password before saving
    hashed_password = hash_password(data['password'])

    # Create and save the new user
    user = User(username=data['username'], password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully!"}), 201

# Login endpoint to generate JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()

    if not user or hash_password(data['password']) != user.password:
        return jsonify({"msg": "Invalid username or password"}), 401

    # Create access token with expiration time
    access_token = create_access_token(identity=user.username, fresh=True, expires_delta=datetime.timedelta(hours=1))
    return jsonify(access_token=access_token), 200

# Protected endpoint to get user details
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# API endpoint to create a new workout
@app.route('/workouts', methods=['POST'])
@jwt_required()
def create_workout():
    current_user = get_jwt_identity()

    data = request.get_json()

    # Validate input
    if not data.get('name') or not data.get('description') or not data.get('difficulty') or data.get('difficulty') not in range(1, 6):
        return jsonify({"msg": "Invalid input. Ensure all fields are present and difficulty is between 1 and 5."}), 400
    
    # Create new workout and associate it with the user
    workout = Workout(
        name=data['name'],
        description=data['description'],
        difficulty=data['difficulty'],
        is_public=data['is_public'],
        username=current_user
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify({"msg": "Workout created successfully!", "workout": {
        "name": workout.name,
        "description": workout.description,
        "difficulty": workout.difficulty,
        "is_public": workout.is_public,
        "username": workout.username
    }}), 201

# API endpoint to modify a workout
@app.route('/workouts/<int:id>', methods=['PUT'])
@jwt_required()
def update_workout(id):
    current_user = get_jwt_identity()

    # Fetch the workout from the database
    workout = Workout.query.get(id)

    if not workout:
        return jsonify({"msg": "Workout not found"}), 404

    # Check if the workout is public or private
    if workout.is_public or workout.username == current_user:
        data = request.get_json()

        # Update workout details
        if 'name' in data:
            workout.name = data['name']
        if 'description' in data:
            workout.description = data['description']
        if 'difficulty' in data and data['difficulty'] in range(1, 6):
            workout.difficulty = data['difficulty']
        if 'is_public' in data:
            workout.is_public = data['is_public']

        db.session.commit()

        return jsonify({"msg": "Workout updated successfully!", "workout": {
            "name": workout.name,
            "description": workout.description,
            "difficulty": workout.difficulty,
            "is_public": workout.is_public,
            "username": workout.username
        }}), 200
    else:
        return jsonify({"msg": "You are not authorized to modify this workout"}), 403

# API endpoint to retrieve all public workouts with filtering and sorting
@app.route('/workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    current_user = get_jwt_identity()

    # Retrieve query parameters for filtering and sorting
    name = request.args.get('name', default=None, type=str)
    difficulty = request.args.get('difficulty', default=None, type=int)
    sort_by_difficulty = request.args.get('sort_by_difficulty', default=None, type=str)

    # Start the query to get all public workouts or private workouts created by the current user
    query = Workout.query.filter(or_(Workout.is_public == True, (Workout.username == current_user)))

    # Search by name (case-insensitive)
    if name:
        query = query.filter(Workout.name.ilike(f'%{name}%'))

    # Filter by difficulty (1-5)
    if difficulty:
        query = query.filter(Workout.difficulty == difficulty)

    # Sort by difficulty (ascending or descending)
    if sort_by_difficulty:
        if sort_by_difficulty.lower() == 'asc':
            query = query.order_by(Workout.difficulty.asc())
        elif sort_by_difficulty.lower() == 'desc':
            query = query.order_by(Workout.difficulty.desc())

    # Fetch results
    workouts = query.all()

    # Return the list of workouts
    return jsonify({
        "workouts": [
            {
                "name": workout.name,
                "description": workout.description,
                "difficulty": workout.difficulty,
                "is_public": workout.is_public,
                "username": workout.username
            } for workout in workouts
        ]
    }), 200


if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
