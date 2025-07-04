import json
import os
from jira import JIRA

# Open your Jira settings
with open('config.json') as f:
    config = json.load(f)

# Connect to Jira using your credentials
jira = JIRA(
    options={'server': config['JIRA_URL']},
    basic_auth=(config['EMAIL'], config['API_TOKEN'])
)

# Ask Jira for tasks in the project
issues = jira.search_issues(f'project={config["PROJECT_KEY"]}', maxResults=30)

# Save useful info
all_issues = []
for issue in issues:
    all_issues.append({
        "key": issue.key,
        "summary": issue.fields.summary,
        "description": issue.fields.description,
        "status": issue.fields.status.name,
        "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
        "created": issue.fields.created
    })

# ✅ Ensure data folder exists before saving
os.makedirs('data', exist_ok=True)

# Save to file
with open('data/raw_issues.json', 'w') as f:
    json.dump(all_issues, f, indent=4)

print("✅ Fetched", len(all_issues), "issues and saved them.")