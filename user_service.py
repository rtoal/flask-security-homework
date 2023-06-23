import sqlite3
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import request, g
import jwt

# This secret for signing tokens should be kept secret. Homework: get this
# from an environment variable.
SECRET = "bfg28y7efg238re7r6t32gfo23vfy7237yibdyo238do2v3"


def get_user_with_credentials(email, password):
    try:
        con = sqlite3.connect("bank.db")
        cur = con.cursor()

        # This is a SQL injection vulnerability:
        # cur.execute(f"""
        #    SELECT email, name, password FROM users where email="{email}"
        #    """)  # BADDDDD
        #

        # This is safe:
        cur.execute("""
            SELECT email, name, password FROM users where email=?""",
                    (email,))

        row = cur.fetchone()
        if row is None:
            return None
        email, name, password_hash = row
        if not pbkdf2_sha256.verify(password, password_hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}
    finally:
        con.close()


def logged_in():
    # A user is logged in iff they have a valid auth token in their cookie
    token = request.cookies.get("auth_token")
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        g.user = data["sub"]
        return True
    except jwt.InvalidTokenError:
        return False


def create_token(email):
    # Create a JWT token containing the user"s email that expires in 60 minutes
    now = datetime.utcnow()
    payload = {"sub": email, "iat": now, "exp": now + timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token
