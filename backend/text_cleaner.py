import json
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    cleaned_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(cleaned_tokens)

def process_issues(input_path='../data/raw_issues.json', output_path='../data/cleaned_issues.json'):
    with open(input_path, 'r') as f:
        issues = json.load(f)

    cleaned_issues = []
    for issue in issues:
        cleaned_issue = {
            "key": issue['key'],
            "status": issue['status'],
            "assignee": issue['assignee'],
            "created": issue['created'],
            "summary_clean": clean_text(issue.get('summary', '')),
            "description_clean": clean_text(issue.get('description', ''))
        }
        cleaned_issues.append(cleaned_issue)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(cleaned_issues, f, indent=4)

    print(f"✅ Cleaned {len(cleaned_issues)} issues and saved to {output_path}")

# ✅ THIS IS IMPORTANT!
if __name__ == "__main__":
    process_issues()
