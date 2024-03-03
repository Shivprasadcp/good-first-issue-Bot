from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import requests
from fpdf import FPDF
import requests
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
# Create your views here.



import requests
from django.shortcuts import render

def fetch_projects(request):
    """
    Fetches repositories for the given GitHub username.
    
    Args:
    - username (str): The GitHub username.
    
    Returns:
    - repositories (list): A list of dictionaries containing repository details.
    """
    repositories = [
        'github.com/deepsourcelabs/good-first-issue',
        'github.com/4paradigm/OpenMLDB',
        'github.com/abpframework/abp',
        'github.com/AcademySoftwareFoundation/openvdb',
        'github.com/activecm/rita',
        'github.com/AdityaMulgundkar/flutter_opencv',
        'github.com/agershun/alasql',
        'github.com/akiran/react-slick',
        'github.com/akxcv/vuera',
        'github.com/alexellis/arkade',
        'github.com/alexfertel/rust-algorithms',
        'github.com/alfasoftware/astra',
        'github.com/alibaba/nacos',
    ]

    projects = []
    for repo_url in repositories:
        # Extract username and repository name from the URL
        username, repo = repo_url.split('/')[-2:]

        # Replace 'YOUR_TOKEN_HERE' with your actual GitHub token
        headers = {
            'Authorization': 'Bearer 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',  # Replace this with your token
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'Sheldon-CodeIt',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        # Construct the GitHub API URL for fetching repository details
        url = f"https://api.github.com/repos/{username}/{repo}"
        
        # Fetch repository details from GitHub API
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            project_details = response.json()
            projects.append(project_details)
        else:
            print(f"Error {response.status_code} occurred while fetching repository details for {repo_url}")

    context = {
        'projects': projects
    }

    return render(request, 'gfi/projects.html', context=context)



def github_repo_details(request, username, repo_name):
    headers = {
            'Authorization': 'Bearer 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',  # Replace this with your token
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'Sheldon-CodeIt',
            'Accept-Encoding': 'gzip, deflate, br'
        }
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        context = {
            "repo_name": data["name"],
            "description": data["description"],
            "stars": data["stargazers_count"],
            "language": data.get("language"),  # Handle potential absence of language
            "open_issues": data["open_issues_count"],
            "last_updated": data["updated_at"],
        }

        # Fetch issues data (optional)
        issues_url = f"{url}/issues" 
        issues_response = requests.get(issues_url, headers=headers)
        if issues_response.status_code == 200:
            context["issues"] = issues_response.json()
            # Optionally fetch additional issue details like discussion and last activity
            for issue in context["issues"]:
                issue_details_url = f"{issue['url']}/comments"
                details_response = requests.get(issue_details_url, headers=headers)
                if details_response.status_code == 200:
                    issue["comments"] = details_response.json()
                    # Extract last activity from comments (assuming latest comment reflects last activity)
                    if issue["comments"]:
                        issue["last_activity"] = issue["comments"][-1]["created_at"]
                else:
                    issue["comments"] = None
                    issue["last_activity"] = None
        else:
            context["issues_error"] = "Failed to fetch issues data"

        return render(request, "gfi/repo_details.html", context)
    else:
        return render(request, "gfi/error.html", {"error_message": "Failed to fetch repository data"})


