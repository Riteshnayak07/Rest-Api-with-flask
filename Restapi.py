from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user data store
users = {}

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user}), 200
    return jsonify({'error': 'User not found'}), 404

# POST - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = data.get('id')
    name = data.get('name')

    if user_id in users:
        return jsonify({'error': 'User ID already exists'}), 400

    users[user_id] = {'name': name}
    return jsonify({'message': 'User created', 'user': users[user_id]}), 201

# PUT - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404

    users[user_id]['name'] = data.get('name', users[user_id]['name'])
    return jsonify({'message': 'User updated', 'user': users[user_id]}), 200

# DELETE - Remove a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify({'message': 'User deleted', 'user': deleted}), 200
    return jsonify({'error': 'User not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
