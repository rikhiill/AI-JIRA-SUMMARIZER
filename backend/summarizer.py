import json
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration
from tqdm import tqdm
from datetime import datetime
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO

print("🔁 Loading T5 model...")
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

def generate_summary(text, max_input=512, max_output=100):
    input_text = "summarize: " + text.strip().replace("\n", " ")
    input_ids = tokenizer.encode(input_text, return_tensors='pt', max_length=max_input, truncation=True)
    summary_ids = model.generate(input_ids, max_length=max_output, min_length=5, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_issues(input_path='data/labeled_issues.json', output_path='data/summarized_issues.json'):
    with open(input_path, 'r') as f:
        issues = json.load(f)

    summarized_issues = []
    print(f"🧠 Summarizing {len(issues)} issues...")
    for issue in tqdm(issues):
        full_text = issue["summary_clean"] + ". " + issue["description_clean"]
        summary = generate_summary(full_text)

        summarized_issue = {
            "key": issue["key"],
            "status": issue["status"],
            "status_tag": issue["status_tag"],
            "assignee": issue["assignee"],
            "created": issue["created"],
            "summary_clean": issue["summary_clean"],
            "description_clean": issue["description_clean"],
            "summary_generated": summary
        }

        summarized_issues.append(summarized_issue)

    os.makedirs("data", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(summarized_issues, f, indent=4)

    # ✅ Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # --- Save to CSV ---
    df = pd.DataFrame(summarized_issues)
    csv_path = f"downloads/summary_{timestamp}.csv"
    df.to_csv(csv_path, index=False)

    # --- Save to PDF ---
    pdf_path = f"downloads/summary_{timestamp}.pdf"
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = [
        Paragraph("📊 AI Jira Summarizer Report", styles["Title"]),
        Paragraph(f"🕒 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]),
        Spacer(1, 12)
    ]

    table_data = [["Key", "Summary", "Assignee", "Status"]]
    for issue in summarized_issues:
        table_data.append([
            issue["key"],
            issue["summary_generated"],
            issue["assignee"],
            issue["status"]
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)
    doc.build(elements)

    with open(pdf_path, "wb") as f:
        f.write(buffer.getvalue())

    print(f"✅ Summarized {len(summarized_issues)} issues")
    print(f"📄 JSON saved to: {output_path}")
    print(f"📊 CSV saved to: {csv_path}")
    print(f"📝 PDF saved to: {pdf_path}")

if __name__ == "__main__":
    summarize_issues()
