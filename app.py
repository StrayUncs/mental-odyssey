from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=10e6)

# Single room data
CHAT_ROOM = 'main'
room_data = {'messages': [], 'users': []}
users_profiles = {}  # Store user profiles with images
users = {}

@app.route("/")
def index():
    return render_template("room.html")

@socketio.on('connect')
def handle_connect():
    session_id = str(uuid.uuid4())
    users[request.sid] = {'name': None, 'session_id': session_id}
    emit('connection_response', {'data': 'Connected to server'})
    # Broadcast updated user list to all clients
    users_data = [{'name': user, 'image': users_profiles.get(user)} for user in room_data['users']]
    emit('users_update', {'users': users_data}, broadcast=True)

@socketio.on('join_room')
def on_join(data):
    username = data['username']
    profile_image = data.get('profile_image', None)  # Get profile image if provided
    
    print(f"User {username} joining, profile image: {profile_image is not None}")
    
    # Store user info
    users[request.sid]['name'] = username
    users_profiles[username] = profile_image  # Store user's profile image
    
    # Join the room
    join_room(CHAT_ROOM)
    
    # Add user to room's user list
    if username not in room_data['users']:
        room_data['users'].append(username)

    # Broadcast updated user list to all clients with profile images
    users_data = [{'name': user, 'image': users_profiles.get(user)} for user in room_data['users']]
    emit('users_update', {'users': users_data}, broadcast=True)
    
    # Notify everyone in the room
    emit('user_joined', {
        'username': username,
        'message': f'{username} has joined the room',
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'users': users_data
    }, room=CHAT_ROOM)
    
    # Send chat history to the new user
    emit('load_chat_history', {
        'messages': room_data['messages'],
        'users': users_data
    })

@socketio.on('send_message')
def on_send_message(data):
    username = users[request.sid]['name']
    message = data['message']
    
    if not username:
        emit('error', {'message': 'Please join first'})
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    message_data = {
        'username': username,
        'message': message,
        'timestamp': timestamp
    }
    
    # Store message
    room_data['messages'].append(message_data)
    
    # Broadcast to all users
    emit('new_message', message_data, room=CHAT_ROOM)


@socketio.on('leave_room')
def on_leave_room():
    if request.sid in users:
        user = users[request.sid]
        username = user['name']
        
        if username and username in room_data['users']:
            # Remove user from room
            room_data['users'].remove(username)
            
            # Broadcast updated user list to all clients
            users_data = [{'name': user, 'image': users_profiles.get(user)} for user in room_data['users']]
            emit('users_update', {'users': users_data}, broadcast=True)
            
            # Notify others
            emit('user_left', {
                'username': username,
                'message': f'{username} has left the room',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'users': users_data
            }, room=CHAT_ROOM)
            
            # Leave the socket room
            leave_room(CHAT_ROOM)
            
            # Reset user info
            users[request.sid]['name'] = None
            
            # Notify the user
            emit('left_room', {'message': 'You have left the room'})

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        user = users[request.sid]
        username = user['name']
        
        if username and username in room_data['users']:
            # Remove user from room
            room_data['users'].remove(username)
            
            # Broadcast updated user list to all clients
            users_data = [{'name': user, 'image': users_profiles.get(user)} for user in room_data['users']]
            emit('users_update', {'users': users_data}, broadcast=True)
            
            # Notify others
            emit('user_left', {
                'username': username,
                'message': f'{username} has left the room',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'users': users_data
            }, room=CHAT_ROOM)
        
        del users[request.sid]

if __name__ == "__main__":
    socketio.run(app, debug=True)
