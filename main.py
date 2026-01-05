import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Get DB configuration from Environment Variables
# This allows you to change secrets without changing code
db_user = os.environ.get('chikamanflask')
db_pass = os.environ.get('$^/j~F{=>f6^BMyp')
db_name = os.environ.get('chikaman')
instance_connection_name = os.environ.get('expense-tracker-483016:us-central1-c:chikaman')  # e.g., project:region:instance

# 2. Configure Database URI
# If running on Cloud Run (INSTANCE_CONNECTION_NAME is set), use Unix Socket.
# If running locally, use TCP (localhost).
if instance_connection_name:
    socket_path = f'/cloudsql/{instance_connection_name}'
    # PostgresSQL example:
    db_uri = f"postgresql+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock={socket_path}/.s.PGSQL.5432"
    # MySQL example:
    # db_uri = f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket={socket_path}"
else:
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_uri = f"postgresql+pg8000://{db_user}:{db_pass}@{db_host}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "API is running and connected to DB!"


if __name__ == "__main__":
    # Cloud Run sets the PORT env var automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
