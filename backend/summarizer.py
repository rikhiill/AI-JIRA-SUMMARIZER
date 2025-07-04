import json
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration
from tqdm import tqdm

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

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(summarized_issues, f, indent=4)

    print(f"✅ Summarized {len(summarized_issues)} issues and saved to {output_path}")

if __name__ == "__main__":
    summarize_issues()
