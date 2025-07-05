from flask import Flask, send_file, jsonify
import os
import zipfile
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>✅ Flask is running! Try /download/pdf or /download/all</h2>"

# --- Standard individual downloads ---
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
    path = "data/summarized_issues.json"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "JSON not found"}), 404

# --- All-in-one ZIP bundle ---
@app.route('/download/all')
def download_all_reports():
    downloads_path = "downloads"
    json_path = "data/summarized_issues.json"
    
    # Get latest PDF and CSV
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

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='jira_summary_bundle.zip'
    )

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
