# Jira Issues Semantic Similarity

This script uses the `requests` library to pull all issues for a project from Jira's REST API. It then uses the `txtai` library to calculate the similarity between the issue descriptions. The script is set up to pull all issues for the project specified in the `JIRA_PROJECT` environment variable that are not marked as "Complete".

## Requirements

- Python 3.6 or higher
- `requests` library
- `txtai` library
- A Jira account with access to the project you want to pull issues from
- Environment variables for your Jira username, API key, base URL, and project

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Create a virtual environment (optional): `python3 -m venv venv`
4. Activate the virtual environment (optional): `source venv/bin/activate`
5. Install the required libraries: `pip install -r requirements.txt`

## Environment Variables

This script requires four environment variables to be set: `JIRA_USER`, `JIRA_API_KEY`, `JIRA_BASE_URL`, and `JIRA_PROJECT`. These should be set to your Jira username, API key, the base URL for your Jira instance, and the project you want to pull issues from, respectively. You can set these variables in a `.env` file in the project directory. An example `.env` file is provided in the repository.

## Usage

To run the script, navigate to the project directory in your terminal and run the following command:

```
python jira_issues_similarity.py
```

The script will pull all issues for the project specified in the `JIRA_PROJECT` environment variable that are not marked as "Complete" and calculate the similarity between the issue descriptions. The results will be printed to the console.

You can modify the JQL query in the script to pull different issues from Jira. JQL is a powerful query language that allows you to search for issues based on a wide range of criteria. For more information on JQL, see the [official Jira documentation](https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-functions/).
