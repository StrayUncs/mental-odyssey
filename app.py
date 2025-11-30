from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import uuid
from agent_setup import run_query  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=10e6)

# Single room data
CHAT_ROOM = 'main'
room_data = {'messages': [], 'users': []}
users_profiles = {}  # Store user profiles with images
hand_raised = {}  # Track hand raised status: {username: timestamp}
speaking_queue = []  # Queue of users who raised hands, in order
current_speaker = None  # The user currently speaking
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
    users_data = [{'name': user, 'image': users_profiles.get(user), 'hand_raised': user in hand_raised} for user in room_data['users']]
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
    
    # Check if user is the first in the speaking queue
    if not speaking_queue or speaking_queue[0] != username:
        emit('error', {'message': 'Only the first person with raised hand can speak'})
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    message_data = {
        'username': username,
        'message': message,
        'timestamp': timestamp
    }
    
    # Store message
    room_data['messages'].append(message_data)
    
    result = run_query(message)
    print("TOOL OUTPUT:", result)
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
            
            # Remove from hand_raised and speaking_queue if present
            if username in hand_raised:
                del hand_raised[username]
            if username in speaking_queue:
                speaking_queue.remove(username)
            
            # Broadcast updated user list to all clients
            users_data = [{'name': user, 'image': users_profiles.get(user), 'hand_raised': user in hand_raised} for user in room_data['users']]
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
            
            # Remove from hand_raised and speaking_queue if present
            if username in hand_raised:
                del hand_raised[username]
            if username in speaking_queue:
                speaking_queue.remove(username)
            
            # Broadcast updated user list to all clients
            users_data = [{'name': user, 'image': users_profiles.get(user), 'hand_raised': user in hand_raised} for user in room_data['users']]
            emit('users_update', {'users': users_data}, broadcast=True)
            
            # Notify others
            emit('user_left', {
                'username': username,
                'message': f'{username} has left the room',
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'users': users_data
            }, room=CHAT_ROOM)
        
        del users[request.sid]

@socketio.on('raise_hand')
def on_raise_hand():
    if request.sid not in users:
        return
    
    username = users[request.sid]['name']
    if not username:
        emit('error', {'message': 'Please join first'})
        return
    
    # Add user to hand_raised and speaking_queue if not already there
    if username not in hand_raised:
        hand_raised[username] = datetime.now()
        speaking_queue.append(username)
    
    # Broadcast updated user list with hand raised status
    users_data = [{'name': user, 'image': users_profiles.get(user), 'hand_raised': user in hand_raised} for user in room_data['users']]
    emit('users_update', {'users': users_data}, broadcast=True)
    emit('hand_raised', {'username': username}, room=CHAT_ROOM)
    # Notify all clients about the current speaker (first in queue)
    current_speaker_name = speaking_queue[0] if speaking_queue else None
    emit('current_speaker_update', {'speaker': current_speaker_name}, broadcast=True)

@socketio.on('lower_hand')
def on_lower_hand():
    if request.sid not in users:
        return
    
    username = users[request.sid]['name']
    if not username:
        emit('error', {'message': 'Please join first'})
        return
    
    # Remove user from hand_raised and speaking_queue
    if username in hand_raised:
        del hand_raised[username]
    if username in speaking_queue:
        speaking_queue.remove(username)
    
    # Broadcast updated user list with hand raised status
    users_data = [{'name': user, 'image': users_profiles.get(user), 'hand_raised': user in hand_raised} for user in room_data['users']]
    emit('users_update', {'users': users_data}, broadcast=True)
    emit('hand_lowered', {'username': username}, room=CHAT_ROOM)
    # Notify all clients about the current speaker (first in queue)
    current_speaker_name = speaking_queue[0] if speaking_queue else None
    emit('current_speaker_update', {'speaker': current_speaker_name}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
