import requests
import dotenv
import os
from txtai.embeddings import Embeddings
from pprint import pprint


# Load environment variables
dotenv.load_dotenv()

# Get authentication information from environment variables
username = os.getenv("JIRA_USER")
api_key = os.getenv("JIRA_API_KEY")

embeddings = Embeddings({"path": "sentence-transformers/nli-mpnet-base-v2"})

# Set up authentication
auth = (username, api_key)

# Set up the base URL for the Jira REST API
base_url = os.getenv("JIRA_BASE_URL")
project = os.getenv("JIRA_PROJECT")

# Set up the JQL query to get all issues for a project
jql = f'project = "{project}" AND status NOT IN ("Complete")'

# Set up the startAt parameter for pagination
start_at = 0

# Set up the maxResults parameter for pagination
max_results = 100

# Set up an empty list to store the issues
issues = []

# Loop through the pages of issues until there are no more issues to get
while True:
    # Set up the URL for the search API with the JQL query and pagination parameters
    url = f"{base_url}/search?jql={jql}&startAt={start_at}&maxResults={max_results}"

    # Make the request to the search API with authentication
    response = requests.get(url, auth=auth)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the issues from the response and add them to the list of issues
        issues += response.json()["issues"]

        # Check if there are more issues to get
        if len(issues) < response.json()["total"]:
            # Increment the startAt parameter for the next page of issues
            start_at += max_results
        else:
            # All issues have been retrieved, break out of the loop
            break
    else:
        # The request was not successful, raise an exception
        response.raise_for_status()

# Create 1D array of issue summaries and descriptions
documents = [
    (
        issue["key"],
        str(issue["fields"]["summary"]) + str(issue["fields"]["description"]),
        issue["fields"]["issuetype"]["name"],
    )
    for issue in issues
]

# Index documents
embeddings.index(documents)

# For every issue, find issues that are similar
# A new list will be returned where each row has a list of similar issues and their scores
# If an issue is found to be simalar, remove it from the list of issues to compare against
# This will prevent duplicate issues from being returned
similar = []
for issue in documents:
    # Get similar issues
    results = embeddings.search(issue[1], 10)

    # 80% similarity threshold
    results = [r for r in results if r[1] > 0.8]

    # Remove similar issues from list of issues to compare against
    documents = [d for d in documents if d[0] not in [r[0] for r in results]]

if similar != []:
    # Print similar issues
    pprint(similar)
else:
    print("No similar issues found")
