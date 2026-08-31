from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import uuid

# --- Configuration ---
SERVER_ADDRESS = ('localhost', 8000)

# --- In-memory storage for sessions (simulating database/cache)
# In a real app, this would be a persistent store like Redis or a database.
# Key: session_id, Value: {'user_id': '...', 'username': '...'}
SESSION_STORE = {}

# --- JWT Configuration (for comparison, not fully implemented here for simplicity)
# JWTs are stateless on the server side, but require signing/verification.
# For this example, we focus on the state management aspect of sessions.


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == '/login':
            # Simulate user login
            username = data.get('username')
            password = data.get('password') # In real app, hash and verify

            if username and password == 'password123': # Simple check
                # Create a new session
                session_id = str(uuid.uuid4())
                SESSION_STORE[session_id] = {'user_id': str(uuid.uuid4()), 'username': username}

                # Set session cookie on the client
                self.send_response(200)
                self.send_header('Set-Cookie', f'session_id={session_id}; HttpOnly; Path=/')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Login successful', 'session_id': session_id}).encode('utf-8'))
            else:
                self._set_response(401)
                self.wfile.write(json.dumps({'message': 'Invalid credentials'}).encode('utf-8'))

        elif self.path == '/logout':
            # Get session ID from cookie
            session_id = self._get_session_id_from_cookie()
            if session_id and session_id in SESSION_STORE:
                # Remove session from server-side store
                del SESSION_STORE[session_id]
                self._set_response()
                self.wfile.write(json.dumps({'message': 'Logout successful'}).encode('utf-8'))
            else:
                self._set_response(401)
                self.wfile.write(json.dumps({'message': 'No active session'}).encode('utf-8'))

    def do_GET(self):
        if self.path == '/profile':
            # Get session ID from cookie
            session_id = self._get_session_id_from_cookie()

            if session_id and session_id in SESSION_STORE:
                # Retrieve user data from server-side session store
                user_data = SESSION_STORE[session_id]
                self._set_response()
                self.wfile.write(json.dumps({'message': f'Welcome {user_data.get("username")}', 'user': user_data}).encode('utf-8'))
            else:
                self._set_response(401)
                self.wfile.write(json.dumps({'message': 'Unauthorized'}).encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({'message': 'Not Found'}).encode('utf-8'))

    def _get_session_id_from_cookie(self):
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookies = dict(cookie.strip().split('=') for cookie in cookie_header.split(';'))
            return cookies.get('session_id')
        return None


def run(server_class=HTTPServer, handler_class=RequestHandler, address=SERVER_ADDRESS):
    server_address = address
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on {address}...')
    # This server uses server-side state (SESSION_STORE) to manage sessions.
    # JWTs would delegate state to the client token, requiring less server memory.
    httpd.serve_forever()

if __name__ == '__main__':
    run()
