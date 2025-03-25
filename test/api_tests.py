import requests
import json

# Base URL for the Flask app (change if running on a different host/port)
BASE_URL = "http://127.0.0.1:5000"

# 1. Register a new user
def register_user(username, password):
    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password
    })
    if response.status_code == 201:
        print(f"User {username} registered successfully.")
        print(response.json())
    else:
        print(f"Failed to register user {username}: {response.status_code}")
        print(response.json())

# 2. Login to get JWT token
def login_user(username, password):
    response = requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f"Login successful. JWT Token: {token}")
        return token
    else:
        print(f"Failed to login: {response.status_code}")
        print(response.json())
        return None

# 3. Create a new workout
def create_workout(token, name, description, difficulty, is_public):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/workouts", json={
        "name": name,
        "description": description,
        "difficulty": difficulty,
        "is_public": is_public
    }, headers=headers)
    if response.status_code == 201:
        print(f"Workout '{name}' created successfully.")
        print(response.json())
    else:
        print(f"Failed to create workout: {response.status_code}")
        print(response.json())

# 4. Modify a workout
def modify_workout(token, workout_id, name, description, difficulty, is_public):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{BASE_URL}/workouts/{workout_id}", json={
        "name": name,
        "description": description,
        "difficulty": difficulty,
        "is_public": is_public
    }, headers=headers)
    if response.status_code == 200:
        print(f"Workout ID {workout_id} modified successfully.")
        print(response.json())
    else:
        print(f"Failed to modify workout: {response.status_code}")
        print(response.json())

# 5. Get workouts (only public workouts or user's own if authenticated)
def get_workouts(token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.get(f"{BASE_URL}/workouts", headers=headers)
    if response.status_code == 200:
        print("Workouts retrieved successfully.")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to retrieve workouts: {response.status_code}")
        print(response.json())

# 6. Test the protected resource (to check if JWT token works)
def test_protected_resource(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    if response.status_code == 200:
        print("Protected resource accessed successfully.")
        print(response.json())
    else:
        print(f"Failed to access protected resource: {response.status_code}")
        print(response.json())

# Main testing function
def main():
    # Step 1: Register a new user
    username = "testuser"
    password = "password123"
    register_user(username, password)
    
    # Step 2: Log in to get the JWT token
    token = login_user(username, password)
    if not token:
        return
    
    # Step 3: Create a new workout
    create_workout(token, "Full Body Workout", "A challenging full-body workout.", 4, True)
    
    # Step 4: Modify the workout (you will need to use the actual workout ID here)
    # Assuming the workout ID is 1 (replace with actual ID from your database)
    modify_workout(token, 1, "Updated Full Body Workout", "An easier version of full-body workout.", 3, False)
    
    # Step 5: Retrieve all workouts (will include public ones and the user's own)
    get_workouts(token)
    
    # Step 6: Access the protected resource
    test_protected_resource(token)

# Run the tests
if __name__ == "__main__":
    main()
