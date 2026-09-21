from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# ============================================================
# INTENTIONALLY HARDCODED SECRETS — FOR GITLEAKS TRAINING ONLY
# DO NOT USE REAL CREDENTIALS
# ============================================================

SECRET_KEY = "my-super-secret-api-key-12345"

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_SESSION_TOKEN = (
    "IQoJb3JpZ2luX2VjEAEaCXVzLWVhc3QtMSJHMEUCIQDTRAININGONLY"
)

OPENAI_API_KEY = "sk-proj-TRAINING-ONLY-1234567890abcdef"
STRIPE_API_KEY = "sk_test_TRAINING_ONLY_1234567890abcdef"
SENDGRID_API_KEY = "SG.TRAINING_ONLY_1234567890abcdef"

DB_USERNAME = "admin"
DB_PASSWORD = "SuperSecretDatabasePassword123!"
DB_HOST = "localhost"
DB_NAME = "users"

JWT_SECRET = "jwt-training-secret-987654321"

GITHUB_TOKEN = "ghp_TRAININGONLY1234567890abcdef123456"

app.config["SECRET_KEY"] = SECRET_KEY


def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    conn.execute("""
        INSERT OR IGNORE INTO users (id, username, password)
        VALUES (1, 'admin', 'admin123')
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# INTENTIONALLY VULNERABLE TO SQL INJECTION
# ============================================================
@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()

    query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{password}'
    """

    user = conn.execute(query).fetchone()

    conn.close()

    if user:
        return f"""
        <h2>Login Successful</h2>
        <p>Welcome {user['username']}</p>
        <a href="/">Back</a>
        """

    return """
    <h2>Login Failed</h2>
    <p>Invalid username or password</p>
    <a href="/">Try Again</a>
    """


@app.route("/user")
def user():

    username = request.args.get("username")

    conn = get_db()

    # INTENTIONALLY VULNERABLE SQL QUERY
    query = f"SELECT * FROM users WHERE username = '{username}'"

    user = conn.execute(query).fetchone()

    conn.close()

    if user:
        return {
            "id": user["id"],
            "username": user["username"],
            "password": user["password"]
        }

    return {"error": "User not found"}, 404


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
