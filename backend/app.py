from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
import os
import zipfile
import io
from datetime import timedelta
from datetime import datetime
import csv
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

LOG_FILE = "download_log.csv"

JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # secure this in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

USERS_FILE = "data/users.json"
SUMMARY_FILE = "data/summarized_issues.json"

# Create users.json if not exist
if not os.path.exists(USERS_FILE):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, "w") as f:
        default_user = {
            "admin": bcrypt.generate_password_hash("admin123").decode('utf-8')
        }
        json.dump(default_user, f, indent=2)

@app.route("/")
def home():
    return "<h2>✅ Flask is running! Try /login or /api/summary with token</h2>"

# --- LOGIN ROUTE ---
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if username not in users:
        return jsonify({"error": "User not found"}), 401

    hashed = users[username]
    if not bcrypt.check_password_hash(hashed, password):
        return jsonify({"error": "Invalid password"}), 401

    token = create_access_token(identity=username)
    return jsonify(access_token=token), 200


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # Load existing users or create new file
    if not os.path.exists(USERS_FILE):
        os.makedirs("data", exist_ok=True)
        users = {}
    else:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)

    if username in users:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users[username] = hashed_password

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

    token = create_access_token(identity=username)
    return jsonify(access_token=token), 200



@app.route("/verify-token", methods=["GET"])
@jwt_required()
def verify_token():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Token valid for user: {current_user}"}), 200

# --- PROTECTED APIs ---
@app.route("/api/summary", methods=["GET"])
@jwt_required()
def get_summary():
    if not os.path.exists(SUMMARY_FILE):
        return jsonify({"error": "No summaries found"}), 404

    with open(SUMMARY_FILE, "r") as f:
        data = json.load(f)
        for issue in data:
            issue["summary"] = issue.get("summary_generated", "")
        return jsonify(data), 200

@app.route("/api/update-summary", methods=["POST"])
@jwt_required()
def update_summary():
    try:
        data = request.get_json()
        with open(SUMMARY_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Summary updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- DOWNLOAD ROUTES (Unprotected) ---
@app.route("/download/pdf", methods=["GET"])
def download_pdf():
    pdfs = sorted([f for f in os.listdir("downloads") if f.endswith(".pdf")], reverse=True)
    if pdfs:
        return send_file(os.path.join("downloads", pdfs[0]), as_attachment=True)
    return jsonify({"error": "No PDF found"}), 404

@app.route("/download/csv", methods=["GET"])
def download_csv():
    csvs = sorted([f for f in os.listdir("downloads") if f.endswith(".csv")], reverse=True)
    if csvs:
        return send_file(os.path.join("downloads", csvs[0]), as_attachment=True)
    return jsonify({"error": "No CSV found"}), 404

@app.route("/download/json", methods=["GET"])
def download_json():
    if os.path.exists(SUMMARY_FILE):
        return send_file(SUMMARY_FILE, as_attachment=True)
    return jsonify({"error": "JSON not found"}), 404

@app.route('/download/all', methods=["GET"])
def download_all_reports():
    downloads_path = "downloads"
    json_path = SUMMARY_FILE
    files = sorted(os.listdir(downloads_path), reverse=True)

    latest_pdf = next((f for f in files if f.endswith(".pdf")), None)
    latest_csv = next((f for f in files if f.endswith(".csv")), None)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        if latest_pdf:
            zip_file.write(os.path.join(downloads_path, latest_pdf), latest_pdf)
        if latest_csv:
            zip_file.write(os.path.join(downloads_path, latest_csv), latest_csv)
        if os.path.exists(json_path):
            zip_file.write(json_path, "summary.json")

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='jira_summary_bundle.zip')

@app.route('/download/<file_type>')
@jwt_required()
def download_file(file_type):
    current_user = get_jwt_identity()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Log the event
    log_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(['username', 'file_type', 'timestamp'])  # Header
        writer.writerow([current_user, file_type.upper(), timestamp])

    # ✅ Continue with existing download logic (PDF, CSV, etc.)
    if file_type == 'pdf':
        return send_file('generated_report.pdf', as_attachment=True)
    elif file_type == 'csv':
        return send_file('generated_report.csv', as_attachment=True)
    elif file_type == 'json':
        return send_file('summarized_issues.json', as_attachment=True)
    elif file_type == 'all':
        return send_file('summaries_bundle.zip', as_attachment=True)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400


# --- Main Runner ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
