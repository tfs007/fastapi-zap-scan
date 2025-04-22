from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import os

app = FastAPI(title="Vulnerable FastAPI App")

# Create a simple in-memory SQLite database with a users table
def setup_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    ''')
    # Insert some sample data
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin123')")
    cursor.execute("INSERT INTO users VALUES (2, 'user', 'password123')")
    conn.commit()
    return conn

# Initialize database connection
db_conn = setup_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Vulnerable FastAPI App</title>
        </head>
        <body>
            <h1>Welcome to the Vulnerable FastAPI App</h1>
            <p>This application contains intentional security vulnerabilities for OWASP ZAP scanning.</p>
            <ul>
                <li><a href="/user-search">User Search (SQL Injection Vulnerability)</a></li>
                <li><a href="/sensitive-data">Sensitive Data Exposure</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/user-search", response_class=HTMLResponse)
async def user_search_form():
    return """
    <html>
        <head>
            <title>User Search</title>
        </head>
        <body>
            <h1>User Search</h1>
            <p>Search for users by username (try: <code>admin' OR '1'='1</code> for SQL injection)</p>
            <form action="/user-search-results" method="get">
                <input type="text" name="username" placeholder="Enter username">
                <input type="submit" value="Search">
            </form>
        </body>
    </html>
    """

@app.get("/user-search-results", response_class=HTMLResponse)
async def user_search_results(username: str = ""):
    # VULNERABILITY: SQL Injection
    # This is intentionally vulnerable - DO NOT use this in production!
    query = f"SELECT id, username FROM users WHERE username LIKE '{username}'"
    
    try:
        cursor = db_conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        result_html = "<h1>Search Results</h1>"
        if results:
            result_html += "<ul>"
            for user_id, user_name in results:
                result_html += f"<li>ID: {user_id}, Username: {user_name}</li>"
            result_html += "</ul>"
        else:
            result_html += "<p>No users found</p>"
        
        return f"""
        <html>
            <head>
                <title>Search Results</title>
            </head>
            <body>
                {result_html}
                <p><a href="/user-search">Back to search</a></p>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <head>
                <title>Error</title>
            </head>
            <body>
                <h1>Error</h1>
                <p>An error occurred: {str(e)}</p>
                <p><a href="/user-search">Back to search</a></p>
            </body>
        </html>
        """

@app.get("/sensitive-data", response_class=HTMLResponse)
async def sensitive_data():
    # VULNERABILITY: Sensitive Data Exposure
    return """
    <html>
        <head>
            <title>Sensitive Data</title>
        </head>
        <body>
            <h1>Sensitive Data</h1>
            <div id="sensitive-info">
                <h2>API Keys (Do Not Share!)</h2>
                <ul>
                    <li>AWS_SECRET_KEY: AKIAIOSFODNN7EXAMPLE</li>
                    <li>DATABASE_PASSWORD: super_secret_password123</li>
                    <li>JWT_SECRET: jwt_secret_key_for_token_signing</li>
                </ul>
                <h2>Internal Server Information</h2>
                <ul>
                    <li>Server Version: Ubuntu 20.04 LTS</li>
                    <li>Database: SQLite 3.31.1</li>
                    <li>Internal IP: 192.168.1.100</li>
                </ul>
            </div>
        </body>
    </html>
    """

# Add a header with security misconfiguration
@app.middleware("http")
async def add_insecure_headers(request: Request, call_next):
    response = await call_next(request)
    # VULNERABILITY: Security Misconfiguration - Insecure Headers
    response.headers["X-Powered-By"] = "FastAPI/0.95.0"
    response.headers["Server"] = "Nginx/1.18.0 (Ubuntu)"
    # Missing security headers
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
