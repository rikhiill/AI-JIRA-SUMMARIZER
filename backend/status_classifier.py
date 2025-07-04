import json
import os

# Rule-based status classifier
def classify_status(jira_status):
    jira_status = jira_status.lower()
    if "done" in jira_status or "closed" in jira_status or "resolved" in jira_status:
        return "Completed"
    elif "progress" in jira_status or "working" in jira_status:
        return "In Progress"
    else:
        return "To Do"

def process_status(input_path='../data/cleaned_issues.json', output_path='../data/labeled_issues.json'):
    with open(input_path, 'r') as f:
        issues = json.load(f)

    labeled_issues = []
    for issue in issues:
        issue['status_tag'] = classify_status(issue['status'])
        labeled_issues.append(issue)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(labeled_issues, f, indent=4)

    print(f"✅ Tagged {len(labeled_issues)} issues and saved to {output_path}")

# Run the function
if __name__ == "__main__":
    process_status()
