from flask import Flask, session, redirect, request, render_template
from authlib.integrations.flask_client import OAuth
import os
from functools import wraps
import jwt

app = Flask(__name__)
app.secret_key = os.urandom(24)
oauth = OAuth(app)

keycloak = oauth.register(
    name='keycloak',
    server_metadata_url=f'http://keycloak:8080/realms/{os.getenv("KEYCLOAK_REALM")}/.well-known/openid-configuration',
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    client_kwargs={'scope': 'openid profile roles'},
)

# Default text for home page
HOME_TEXT = "Bienvenue sur l'application A !"

def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if session.get('user'):
                if role:
                    user_roles = session['user'].get('roles', [])
                    if role not in user_roles:
                        return "Unauthorized", 403
                return fn(*args, **kwargs)
            return redirect('/login')
        return decorated_view
    return wrapper


@app.route('/', methods=['GET', 'POST'])
@login_required()
def home():
    global HOME_TEXT
    if request.method == 'POST':
        if "admin" in session['user'].get('roles',[]):
            HOME_TEXT = request.form['home_text']
    is_admin = "admin" in session['user'].get('roles', [])
    return render_template('home.html', home_text=HOME_TEXT, admin=is_admin)



@app.route('/login')
def login():
    redirect_uri = request.base_url.replace('/login', '/callback')
    return keycloak.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = keycloak.authorize_access_token()
    user_info = token.get('userinfo')
    access_token = token.get('access_token')
    decoded_token = jwt.decode(access_token, options={"verify_signature": False})
    roles = decoded_token.get('realm_access').get('roles')
    session['user'] = {
        'name': user_info.get('name', 'User'),
        'roles': roles
    }
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)