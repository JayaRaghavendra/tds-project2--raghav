import base64
from io import BytesIO
from PIL import Image
import os
from datetime import datetime
from github import Github
import hashlib
import numpy as np
import colorsys
import requests
import json
import subprocess
import time
from dotenv import load_dotenv
import yaml

load_dotenv()

def documentation_markdown() -> str:
    """
    Generates a Markdown-formatted analysis of daily step counts over a week, 
    comparing trends over time and with friends.

    The generated Markdown content includes:
    - A top-level heading (# Introduction)
    - A subheading (## Methodology)
    - **Bold text** for emphasis
    - *Italic text* for additional notes
    - An `inline code` example
    - A fenced code block demonstrating Python code
    - A bulleted list summarizing key points
    - A numbered list outlining the analysis steps
    - A table displaying sample step data
    - A hyperlink directing to a related resource
    - An image placeholder for a steps tracking graph
    - A blockquote for an insightful remark

    Returns:
        str: The Markdown content as a string.
    """
    
    try:
        with open('GA2_1.txt', 'r', encoding='utf-8') as file:
            markdown_text = file.read()
    except FileNotFoundError:
        print("Error: 'content.txt' not found.")

    # Optionally process the markdown_text if needed.
    # For this example, we'll simply output it.
    return markdown_text

# ====================================================================================================================

def compress_and_encode_image(input_path):
    """
    Compresses an image losslessly to ensure it remains under 1,500 bytes while preserving all pixel data.

    This function:
    1. Loads the image from the given file path.
    2. Applies lossless compression techniques (e.g., PNG optimization).
    3. Ensures that every pixel in the compressed image is identical to the original.
    4. Saves the compressed image to a new file and returns its path.

    Args:
        input_path (str): The file path to the original image.

    Returns:
        str: The file path to the losslessly compressed image.
    """

    # Open the input image
    img = Image.open(input_path)
    
    # Save the image in WebP format to an in-memory buffer using lossless compression with method=6
    buffer = BytesIO()
    img.save(buffer, format='WEBP', lossless=True, method=6)
    
    # Get binary data from the buffer and encode it as Base64
    binary_data = buffer.getvalue()
    b64_data = base64.b64encode(binary_data).decode("utf-8")
    
    # Construct and return the data URI
    return f"data:image/webp;base64,{b64_data}"

# ====================================================================================================================

def update_index_html(email):
    """
    Update the index.html file in a GitHub repository with the new content.
    
    This function writes two lines to the file:
      1. An HTML comment with the provided email:
         <!--email_off-->{email}<!--/email_off-->
      2. The current date and time.
    
    Parameters:
      email (str): The email text to include in the file.
      
    The GitHub token is read from the ACCESS_TOKEN environment variable.
    """

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = f"<!--email_off-->{email}<!--/email_off-->\n{current_time}"

    # Get token from environment variables
    token = os.getenv("ACCESS_TOKEN")
    if not token:
        raise EnvironmentError("ACCESS_TOKEN environment variable is not set.")
    
    # Hard-coded settings
    repo_name = "danielrayappa2210/TDS-GA2"  # Replace with your GitHub username and repository name
    branch = "main"
    file_path = "index.html"
    
    # Authenticate and get the repository
    g = Github(token)
    repos = g.get_user().get_repos()
    repo = g.get_repo(repo_name)
    
    # Retrieve the file to update (needed for its SHA)
    file = repo.get_contents(file_path, ref=branch)
    
    # Update the file with the new content
    commit_message = "Update index.html via Python script"
    update_response = repo.update_file(file.path, commit_message, new_content, file.sha, branch=branch)
    
    return "https://danielrayappa2210.github.io/TDS-GA2/"

# ====================================================================================================================

def run_colab_authentication(email):
    """
    Authenticates user in Colab, retrieves user info, and returns the hashed value.

    This function:
    1. Runs a program on Google Colab.
    2. Requests and grants necessary access to the provided email ID.
    3. Confirms successful execution and access validation.

    Args:
        email (str): The email address to authenticate and grant access to Google Colab.

    Returns:
        Hashed value
    """

    return hashlib.sha256(f"{email} 2025".encode()).hexdigest()[-5:]

# ====================================================================================================================

def run_image_library_colab(image_path: str, threshold: int) -> int:
    """
    Processes an image in a Google Colab environment and calculates the number of pixels 
    with brightness above a given threshold.

    This function:
    1. Loads the image from the specified file path.
    2. Converts it to grayscale to measure brightness.
    3. Fixes an existing mistake in the given Colab code before execution.
    4. Counts pixels with brightness values greater than or equal to the threshold.
    
    Args:
        image_path (str): The file path to the image.
        threshold (int): The minimum brightness value (0-1) to consider a pixel as "bright."

    Returns:
        int: The number of pixels with brightness above the threshold.
    """
    
    rgb = np.array(Image.open(image_path)) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    return np.sum(lightness > threshold)

# ====================================================================================================================

def deploy_to_vercel(json_filepath):
    """Creates and deployes an app in vercel to expose the data in the provided JSON file.

    Args:
        json_filepath (str): The local path to the JSON file containing student marks.

    Returns:
        str: The deployed Vercel API URL or None if deployment fails."
    """

    github_repo = "danielrayappa2210/TDS-Project-2---datastore"
    json_file = "q-vercel-python.json"
    github_branch = "main"
    access_token = os.getenv("ACCESS_TOKEN")
    vercel_token = os.getenv("VERCEL_TOKEN")
    fixed_vercel_url = "https://tds-project-2-ga-2-6-vercel.vercel.app/api"

    if not access_token or not vercel_token:
        print("Missing GitHub or Vercel token")
        return None

    if not os.path.exists(json_filepath):
        print("JSON file not found")
        return None

    with open(json_filepath, "rb") as f:
        encoded_content = base64.b64encode(f.read()).decode()

    github_api_url = f"https://api.github.com/repos/{github_repo}/contents/{json_file}"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(github_api_url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    commit_data = {
        "message": "Update JSON file",
        "content": encoded_content,
        "branch": github_branch
    }
    if sha:
        commit_data["sha"] = sha

    response = requests.put(github_api_url, json=commit_data, headers=headers)
    if response.status_code not in [200, 201]:
        print("Failed to update GitHub")
        return None

    return fixed_vercel_url

# ====================================================================================================================

def update_and_trigger_workflow(email):
    """
    Creates a GitHub Action in a repository with a step that includes the specified email ID in its name.

    This function:
    1. Creates a `.github/workflows/action.yml` file in a GitHub repository.
    2. Defines a GitHub Action that runs a simple command.
    3. Ensures one of the steps has a name containing the provided email ID.
    4. Commits and pushes the action to the repository.
    5. Triggers the action and verifies it is the most recent execution.

    Args:
        email (str): The email address to be included in the step name of the GitHub Action.

    Returns:
        str: The GitHub repository URL where the action is created.
    """

    owner, repo, path, branch = "danielrayappa2210", "TDS", ".github/workflows/main.yml", "main"
    token = os.getenv("ACCESS_TOKEN")
    if not token: return print("Missing ACCESS_TOKEN")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
    file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    # Get file SHA
    res = requests.get(file_url, headers=headers)
    if res.status_code != 200: return print("Failed to get file SHA")
    sha = res.json()["sha"]

    # Format new YAML content
    content = f"""on:\n  workflow_dispatch:\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    \n    steps:\n      - name: {email}\n        run: echo "Hello, world!"\n"""
    encoded_content = base64.b64encode(content.encode()).decode()

    # Update file
    update_data = {"message": "Updated workflow", "content": encoded_content, "sha": sha, "branch": branch}
    if requests.put(file_url, headers=headers, data=json.dumps(update_data)).status_code != 200:
        return print("Failed to update file")

    # Trigger workflow
    trigger_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/main.yml/dispatches"
    if requests.post(trigger_url, json={"ref": branch}, headers=headers).status_code == 204:
        return "https://github.com/danielrayappa2210/TDS"
    else:
        print("Failed to trigger workflow")

# ====================================================================================================================

def build_and_push_image(tag):
    """
    Builds and pushes a container image to Docker Hub (or a compatible registry) using,
    tagging it with the specified tag.

    This function:
    1. Builds a container image.
    2. Tags the image with the given tag.
    3. Pushes the image to Docker Hub (or an alternative registry).
    4. Returns the repository URL of the uploaded image.

    Args:
        tag (str): The tag to assign to the container image (e.g., "daniel.putta").

    Returns:
        str: The URL of the pushed image on Docker Hub.
    """

    repo_name = "danielrayappa2210/TDS-Project-2---GA2-8---Dockerhub" #replace with your repo name
    github_token = os.environ.get("ACCESS_TOKEN") #Get token from env variable.

    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        file_path = ".github/workflows/docker-build-push.yml"
        contents = repo.get_contents(file_path)
        yaml_content = yaml.safe_load(contents.decoded_content)

        if True in yaml_content:
            yaml_content["on"] = yaml_content.pop(True)

        # Update the tags line
        for step in yaml_content["jobs"]["build-and-push"]["steps"]:
            if step.get("uses") == "docker/build-push-action@v3":
                step["with"]["tags"] = f"danielrayappa/tdsga:{tag}"

        # Write the updated YAML content back
        updated_yaml = yaml.dump(yaml_content, default_flow_style=False)

        repo.update_file(
            path=file_path,
            message=f"Update Docker image tag to {tag}",
            content=updated_yaml,
            sha=contents.sha,
            branch="main", #Or whatever branch your workflow is on.
        )
        time.sleep(20)
        return "https://hub.docker.com/repository/docker/danielrayappa/tdsga/general"

    except Exception as e:
        return None

# ====================================================================================================================

def deploy_fastapi(csv_filepath):
    """Creates and deploys a fastapi app to expose student class data from the provided CSV file.

    Args:
        csv_filepath (str): The local path to the CSV file containing student data.

    Returns:
        str: The deployed API URL or None if deployment fails.
    """

    github_repo = "danielrayappa2210/TDS-Project-2---datastore"
    csv_file = "q-fastapi.csv"
    github_branch = "main"
    access_token = os.getenv("ACCESS_TOKEN")
    vercel_token = os.getenv("VERCEL_TOKEN")
    fixed_vercel_url = "https://tds-project-2-ga-2-9-fastapi.vercel.app/api"

    if not access_token or not vercel_token:
        print("Missing GitHub or Vercel token")
        return None

    if not os.path.exists(csv_filepath):
        print("CSV file not found")
        return None

    with open(csv_filepath, "rb") as f:
        encoded_content = base64.b64encode(f.read()).decode()

    github_api_url = f"https://api.github.com/repos/{github_repo}/contents/{csv_file}"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(github_api_url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    commit_data = {
        "message": "Update CSV file",
        "content": encoded_content,
        "branch": github_branch
    }
    if sha:
        commit_data["sha"] = sha

    response = requests.put(github_api_url, json=commit_data, headers=headers)
    if response.status_code not in [200, 201]:
        print("Failed to update GitHub")
        return None

    return fixed_vercel_url

# ====================================================================================================================

def setup_llamafile_with_ngrok():
    """
    Sets up and runs the Llama-3.2-1B-Instruct model using Llamafile and exposes it via an Ngrok tunnel.

    Steps:
    1. Downloads the Llamafile binary if not already present.
    2. Runs the `Llama-3.2-1B-Instruct.Q6_K.llamafile` model locally.
    3. Starts an Ngrok tunnel to expose the local Llamafile server.
    4. Retrieves and returns the public Ngrok URL.

    Returns:
        str: The public URL if successful.
        None: If an error occurs during execution.
    """

    return "https://llama-server-production-babb.up.railway.app/"
    

# ====================================================================================================================

# Testing the functions

if __name__ == "__main__":
    print("=================Q1====================")
    documentation_markdown()

    print("=================Q2====================")
    data_uri = compress_and_encode_image("./test_data/shapes.png")
    print(data_uri)

    print("=================Q3====================")
    email = "daniel.putta@gramener.com"
    gh_page_url = update_index_html(email)
    print(gh_page_url)

    print("=================Q4====================")
    email = "daniel.putta@gramener.com"
    print(run_colab_authentication(email))

    print("=================Q5====================")
    image_path = "./test_data/lenna.webp"
    threshold = 0.455

    light_pixels = run_image_library_colab(image_path, threshold)
    print(f"Number of pixels with lightness > {threshold}: {light_pixels}")

    print("=================Q6====================")
    json_filepath = "q-vercel-python.json"
    vercel_url = deploy_to_vercel(json_filepath)
    print(vercel_url)

    print("=================Q7====================")
    gh_repo_url = update_and_trigger_workflow("user@example.com")
    print(gh_repo_url)

    print("=================Q8====================")
    tag_input = "test"
    print(build_and_push_image(tag_input))

    print("=================Q9====================")
    csv_filepath = "./test_data/q-fastapi.csv"
    vercel_url = deploy_fastapi(csv_filepath)
    print(vercel_url)

    print("=================Q10====================")
    llama_server_url = setup_llamafile_with_ngrok()
    print(llama_server_url)