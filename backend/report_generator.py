import json
import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Create downloads/ folder if missing
OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Timestamp for filenames
now_str = datetime.now().strftime("%d-%m-%Y_%I-%M%p")

# Define output paths
PDF_OUTPUT = os.path.join(OUTPUT_DIR, f"summary_{now_str}.pdf")
CSV_OUTPUT = os.path.join(OUTPUT_DIR, f"summary_{now_str}.csv")
INPUT_PATH = "data/summarized_issues.json"

# -------- Generate PDF --------
def generate_pdf(issues):
    c = canvas.Canvas(PDF_OUTPUT, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "AI Jira Issue Summary Report")
    y -= 30
    c.setFont("Helvetica", 10)

    for i, issue in enumerate(issues, start=1):
        if y < 100:
            c.showPage()
            y = height - 50
        c.drawString(50, y, f"{i}. {issue['key']} - {issue['status_tag']}")
        y -= 15
        c.drawString(70, y, f"Summary: {issue['summary_clean']}")
        y -= 15
        c.drawString(70, y, f"Generated: {issue['summary_generated']}")
        y -= 25

    c.save()
    print(f"✅ PDF report saved to {PDF_OUTPUT}")

# -------- Generate CSV --------
def generate_csv(issues):
    df = pd.DataFrame([{
        "Issue Key": i['key'],
        "Status": i['status'],
        "Assignee": i['assignee'],
        "Created": i['created'],
        "Original Summary": i['summary_clean'],
        "Generated Summary": i['summary_generated']
    } for i in issues])

    df.to_csv(CSV_OUTPUT, index=False)
    print(f"✅ CSV report saved to {CSV_OUTPUT}")

# -------- Run manually --------
if __name__ == "__main__":
    with open(INPUT_PATH, "r") as f:
        issues = json.load(f)

    generate_pdf(issues)
    generate_csv(issues)
