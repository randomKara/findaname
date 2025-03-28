from flask import Flask, session, redirect, request, render_template, jsonify
from authlib.integrations.flask_client import OAuth
import os
from functools import wraps
import jwt

app = Flask(__name__)
app.secret_key = os.urandom(24)
oauth = OAuth(app)

keycloak = oauth.register(
    name='keycloak',
    server_metadata_url=f'https://keycloak:8443/realms/{os.getenv("KEYCLOAK_REALM")}/.well-known/openid-configuration',
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    client_kwargs={
        'scope': 'openid profile roles',
        'verify': False  # Pour le certificat auto-signé en développement
    },
)

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not session.get('user'):
            return redirect('/login')
        return fn(*args, **kwargs)
    return decorated_view

@app.route('/')
@login_required
def home():
    return render_template('home.html', 
                         username=session['user'].get('name', 'Unknown'),
                         authenticated=True)

@app.route('/login')
def login():
    redirect_uri = request.base_url.replace('/login', '/callback')
    return keycloak.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = keycloak.authorize_access_token()
    user_info = token.get('userinfo')
    access_token = token.get('access_token')
    
    try:
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        roles = decoded_token.get('realm_access', {}).get('roles', [])
    except:
        roles = []
    
    session['user'] = {
        'name': user_info.get('name', 'User'),
        'roles': roles
    }
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 