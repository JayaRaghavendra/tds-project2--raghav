import requests
import pandas as pd 
import httpx
from bs4 import BeautifulSoup
import json
from urllib.parse import urlencode
import re
from datetime import datetime, timedelta, timezone
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv
from github import Github, GithubException
import camelot
import pymupdf4llm
from llm_utils import *

load_dotenv()

# ====================================================================================================================

# Define the session and headers
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_ducks_sum(page_number: int) -> int:
    """
    Counts the total number of ducks (players out for 0 runs) on a specific page of ESPN Cricinfo's ODI batting statistics.

    This function automates the extraction and analysis of ODI batting statistics from ESPN Cricinfo, focusing on counting 
    the number of ducks across players on a given page. It navigates to the specified page number of the paginated stats, 
    uses Google Sheets' IMPORTHTML function to import the table of batting data, and identifies the column that represents 
    the number of ducks (labeled as "0"). It then sums the values in that column to determine the total number of ducks for 
    the specified page.

    Args:
        page_number (int): The page number of the ESPN Cricinfo ODI batting stats to fetch and analyze.

    Returns:
        int: The total number of ducks (players out for 0 runs) across all players on the specified page.
    """

    url = f"https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page={page_number};template=results;type=batting"

    # Fetch the HTML content using the session and headers defined earlier
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    # Read the tables from the HTML content
    tables = pd.read_html(response.text)
    
    # Convert the specific table to DataFrame
    t = pd.DataFrame(tables[2])
    
    # Return the sum of the '0' column
    return t['0'].astype(int).sum()

# ====================================================================================================================

def fetch_imdb_movies(min_rating: float, max_rating: float) -> list:
    """
    Fetches and filters movie data from IMDb based on a specified rating range.

    This function interacts with IMDb's search results to retrieve up to the first 25 movie titles 
    that fall within the given rating range. It extracts relevant details such as the movie ID, 
    title, release year, and rating, structuring the data into a JSON-formatted list.

    Args:
        min_rating (float): The minimum IMDb rating to filter movies.
        max_rating (float): The maximum IMDb rating to filter movies.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
            - "id" (str): IMDb unique identifier for the movie.
            - "title" (str): The official movie title.
            - "year" (str): The release year of the movie.
            - "rating" (str): The IMDb user rating of the movie.

    Example:
        fetch_imdb_movies(2.0, 6.0)
        [
            { "id": "tt1234567", "title": "Movie 1", "year": "2021", "rating": "5.8" },
            { "id": "tt7654321", "title": "Movie 2", "year": "2019", "rating": "6.2" }
        ]
    
    Notes:
        - The function scrapes IMDb search results and parses the extracted data.
        - Only the first 25 matching titles are returned.
        - The movie ID is derived from the IMDb URL (e.g., 'tt10078772' from the href attribute).
    
    """

    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"  # Pretend to be a regular browser
    }

    url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find_all("li", class_="ipc-metadata-list-summary-item", limit=25)

    final_out = []
    pattern = re.compile(r"^sc.*dli-title-metadata-item$")
    for movie in movies:
        temp_dict = {}
        temp_dict['id'] = movie.find("a", class_="ipc-title-link-wrapper").get("href").split('/')[2]
        temp_dict['title'] = movie.find("h3", class_="ipc-title__text").text.strip()
        temp_dict['year'] = movie.find_all("span", class_=pattern)[0].text.strip('-').strip()
        temp_dict['rating'] = movie.find_all("span", class_="ipc-rating-star--rating")[0].text
        final_out.append(temp_dict)

    final_out = [{k: v.replace("–", "") if isinstance(v, str) else v for k, v in movie.items()} for movie in final_out]
    return final_out

# ====================================================================================================================

def country_outline_api_endpoint():
    """
    Retrieves the API endpoint URL for a FastAPI service that generates a structured Markdown outline of a Wikipedia page for a specified country.

    This function does not accept any parameters and simply returns the API URL where the service is hosted.

    API Functionality:
    - Accepts a country name as a query parameter (`?country=`).
    - Fetches the corresponding Wikipedia page for that country.
    - Extracts all headings (H1 to H6) while maintaining their hierarchical structure.
    - Formats the extracted headings into a Markdown-based outline.
    - Enables Cross-Origin Resource Sharing (CORS) to allow unrestricted GET requests from any origin.

    Returns:
        str: The URL of the API endpoint where users can request structured country outlines.
    """
    return "https://tds-project-2-ga-4-3.vercel.app/api/outline"

# ====================================================================================================================

def get_forecast_description(required_city):
    """
    Fetches the weather forecast for a given city using the BBC Weather API.

    This function retrieves the locationId of the specified city through the BBC Weather locator service.
    It then queries the weather broker API to obtain the forecast data, extracting relevant details 
    such as the local date and enhanced weather description. The resulting data is formatted into a 
    JSON object where each date maps to its respective weather condition.

    Args:
        required_city (str): The name of the city for which the weather forecast is requested.

    Returns:
        dict: A JSON-formatted dictionary containing the weather forecast.
              Each key is a date (YYYY-MM-DD) and its value is the corresponding weather description.

    Example:
        fetch_weather_forecast("Osaka")
        {
            "2025-01-01": "Sunny with scattered clouds",
            "2025-01-02": "Partly cloudy with a chance of rain",
            "2025-01-03": "Overcast skies"
        }

    Notes:
        - The function first fetches the city's locationId before retrieving the weather forecast.
        - It extracts only the essential details (date and weather description) for structured output.
        - Ensure the BBC Weather API key is properly configured before calling the function.
    
    """

    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
        'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
        's': required_city,
        'stack': 'aws',
        'locale': 'en',
        'filter': 'international',
        'place-types': 'settlement,airport,district',
        'order': 'importance',
        'a': 'true',
        'format': 'json'
    })
    result = requests.get(location_url).json()
    url = 'https://www.bbc.com/weather/'+result['response']['results']['results'][0]['id']
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    daily_summary = soup.find('div', attrs={'class': 'wr-day-summary'})
    daily_summary_list = re.findall('[a-zA-Z][^A-Z]*', daily_summary.text) #split the string on uppercase
    daily_high_values = soup.find_all('span', attrs={'class': 'wr-day-temperature__high-value'}) 
    datelist = pd.date_range(datetime.today(), periods=len(daily_high_values)).tolist()
    datelist = [datelist[i].date().strftime('%y-%m-%d') for i in range(len(datelist))]
    zipped = zip(datelist, daily_summary_list)
    df = pd.DataFrame(list(zipped), columns=['Date', 'Summary'])
    # Convert to dictionary with date as key
    json_data = df.set_index('Date')['Summary'].to_dict()
  
    json_string = json.dumps(json_data, indent=2)

    return json_string

# ====================================================================================================================

def get_maximum_latitude(country,city):
    """
    Fetches the maximum latitude of the bounding box for a given city in a specified country 
    using the Nominatim API.

    This function sends a GET request to the Nominatim API to retrieve geospatial data 
    for the specified city and country. It extracts the bounding box coordinates and returns 
    the maximum latitude value. If multiple results are found, the function filters the 
    results based on relevant identifiers to select the most appropriate city instance.

    Args:
        country (str): The name of the country where the city is located.
        city (str): The name of the city for which the maximum latitude is required.

    Returns:
        float: The maximum latitude of the city's bounding box.

    Example:
        get_max_latitude("India", "Ahmedabad")
        Output: 23.1453  (Example value, actual result may vary)

    Notes:
        - The function makes a request to the Nominatim API with appropriate query parameters.
        - The response is parsed to extract the bounding box coordinates.
        - Ensure compliance with Nominatim's usage policies, including rate limits and attribution.
        - The function assumes the first matching result is the most relevant unless filtering is applied.

    """

    locator = Nominatim(user_agent="myGeocoder")
    inp_location=f'{country},{city}'
    location = locator.geocode(inp_location)
    location.raw,location.point,location.longitude,location.latitude,location.altitude,location.address
    return location.raw['boundingbox'][1]

# ====================================================================================================================

def fetch_most_recent_link(keyword: str, min_points: int) -> str:
    """
    Fetches the latest Hacker News post that mentions a specified keyword and meets a minimum points threshold 
    using the HNRSS API.

    This function sends a request to the HNRSS API to retrieve recent posts, filters them based on the provided 
    keyword and minimum points, and returns the link to the most relevant post.

    Args:
        keyword (str): The topic or keyword to search for in Hacker News posts.
        min_points (int): The minimum number of points a post must have to be considered relevant.

    Returns:
        str: The URL of the latest Hacker News post that meets the criteria. If no such post is found, returns an empty string.

    Example:
        get_hacker_news_post("OpenAI", 86)
        Output: "https://news.ycombinator.com/item?id=12345678"  (Example URL, actual result may vary)

    Notes:
        - The function queries the HNRSS API for recent posts.
        - Posts are filtered to match the given keyword and meet the minimum points threshold.
        - The most recent qualifying post is selected, and its URL is returned.
        - Ensure proper handling of API rate limits and network errors.

    """

    # Construct the RSS feed URL
    rss_url = f"https://hnrss.org/newest?q={keyword}&points>{min_points}"

    # Fetch the RSS feed
    response = httpx.get(rss_url)
    response.raise_for_status()

    # Parse the RSS feed
    soup = BeautifulSoup(response.text)

    # Find the most recent <item>
    most_recent_item = soup.find('item')

    # Extract the <link> tag inside the most recent <item>
    most_recent_link = most_recent_item.find('link').next_sibling.strip()

    return most_recent_link

# ====================================================================================================================

def get_most_recent_valid_user(location, min_followers, max_date_time):
    """
    Retrieves the creation date of the newest GitHub user located in a specified city with more than a given number of followers.

    This function queries the GitHub API to find users in a specific location who have at least the specified number of followers.
    It then filters the results based on the provided maximum account creation date and returns the creation date of the newest user.

    Args:
        location (str): The city to search for GitHub users (e.g., "Bangalore").
        min_followers (int): The minimum number of followers a user must have to be considered.
        max_date_time (str): The latest possible account creation date (ISO 8601 UTC format, e.g., "2024-01-01T00:00:00Z").

    Returns:
        str: The ISO 8601 formatted creation date of the newest GitHub user who meets the criteria. 
             Returns an empty string if no such user is found.

    Example:
        get_newest_github_user("Bangalore", 110, "2025-01-01T00:00:00Z")
        Output: "2024-12-15T10:30:45Z"  (Example date, actual result depends on GitHub API response)

    Notes:
        - Uses GitHub's search API to fetch users based on location and minimum follower count.
        - Filters users by the provided max_date_time to find the newest account.
        - Handles API rate limits and errors gracefully.
        - Requires authentication via GitHub token for higher request limits.

    """

    headers = {"Authorization": f"Bearer {os.getenv("ACCESS_TOKEN")}", "Content-Type": "application/json"}
    query = f"location:{location} followers:>{min_followers}"
    per_page = 100  # Max allowed
    cursor = None
    user_dates = []
    GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

    # Convert to datetime (handling 'Z' as UTC)
    max_date_time = datetime.strptime(max_date_time, "%Y-%m-%dT%H:%M:%SZ")

    while True:
        # GraphQL query to fetch user details in a single request
        graphql_query = {
            "query": f"""
            query {{
                search(query: "{query}", type: USER, first: {per_page} {f', after: "{cursor}"' if cursor else ''}) {{
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                    edges {{
                        node {{
                            ... on User {{
                                login
                                createdAt
                            }}
                        }}
                    }}
                }}
            }}
            """
        }

        response = requests.post(GITHUB_GRAPHQL_URL, json=graphql_query, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching users: {response.status_code}, {response.json()}")
            break

        data = response.json()
        users = data.get("data", {}).get("search", {}).get("edges", [])
        if not users:
            break

        # Extract created_at datetime
        for user in users:
            if not user["node"]:
                continue
            created_at = user["node"]["createdAt"]
            created_at_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            user_dates.append(created_at_datetime)

        # Pagination handling
        page_info = data["data"]["search"]["pageInfo"]
        cursor = page_info["endCursor"]
        if not page_info["hasNextPage"]:
            break

    # Step 2: Sort dates & get the most recent valid datetime
    user_dates.sort(reverse=True)
    latest_valid_datetime = next((dt for dt in user_dates if dt <= max_date_time), None)

    return latest_valid_datetime.strftime("%Y-%m-%dT%H:%M:%SZ") if latest_valid_datetime else None

# ====================================================================================================================

def create_github_action_workflow(email_id):
    """
    Generates a GitHub Actions workflow file that schedules a daily commit to the repository,
    including a step named with the provided email address.

    This function creates a YAML workflow file in the `.github/workflows/` directory of the
    repository. The workflow is scheduled to run once daily at a fixed time, adds a commit
    to the repository, and includes a step with the specified email address in its name.

    Args:
        email_id (str): The email address to be included in the name of one of the workflow steps.

    Returns:
        str: The URL of the GitHub repository where the workflow file has been created.
    """

    token = os.environ.get("ACCESS_TOKEN")
    repo_name = "danielrayappa2210/TDA-Project-2---GA4-8"
    
    if not token or not repo_name:
        raise ValueError("Both GITHUB_TOKEN and REPO_NAME environment variables must be set.")
    
    # Initialize GitHub API client
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Define the path for the workflow YAML file
    file_path = ".github/workflows/daily_action.yml"
    
    # Compute the minute and hour for 60 seconds from now using timezone-aware now()
    time_after_one_min = datetime.now(timezone.utc) + timedelta(seconds=360)
    time_part = time_after_one_min.strftime("%M %H")
    
    # Use wildcards for day of month, month, and day of week to run everyday
    cron_expr = f"{time_part} * * *"
    # Create the YAML content
    yaml_content = f"""name: Daily Append Date

permissions:
  contents: write    
    
on:
  schedule:
    - cron: '{cron_expr}'

jobs:
  append-date:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Append date to txt file for {email_id}
        run: |
          echo "$(date)" >> timestamp.txt
    
      - name: Commit timestamp.txt
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "github-actions@github.com"
          git add timestamp.txt
          git commit -m "Update timestamp.txt" || echo "No changes to commit"
          git push
"""
    commit_message = "Update GitHub Action workflow: daily schedule and email step"
    
    try:
        # Try to fetch the existing file content
        contents = repo.get_contents(file_path)
        # Update the file with new content
        repo.update_file(contents.path, commit_message, yaml_content, contents.sha)
    except GithubException as e:
        # If the file doesn't exist, create it
        if e.status == 404:
            repo.create_file(file_path, commit_message, yaml_content)
        else:
            # Re-raise the exception if it's an unexpected error
            raise
    return "https://github.com/danielrayappa2210/TDA-Project-2---GA4-8"

# ====================================================================================================================

def calculate_total_marks(filepath, group_range_str, filter_marks, main_subject, filter_subject):
    """
    Calculates the total marks in a specified subject for students who meet or exceed a given score in another subject, within a specified group range.

    Parameters:
    - filepath (str): Path to the PDF file containing the student marks table.
    - group_range_str (str): Range of groups to filter, in the format 'start-end' (e.g., '16-45').
    - filter_marks (int): Minimum score threshold for the filter subject.
    - main_subject (str): The subject for which to calculate the total marks.
    - filter_subject (str): The subject used to apply the score filter.

    Returns:
    - int: Total marks in the main subject for students who scored at least 'filter_marks' in the filter subject within the specified group range.
    """

    # Convert the group range string to a tuple of integers
    group_range = tuple(map(int, group_range_str.split('-')))
    
    # Adjust the range to be zero-indexed
    group_range = (group_range[0] - 1, group_range[1])

    # Read the PDF file
    tables = camelot.read_pdf(filepath, pages="all")

    # Initialize an empty DataFrame
    subject_df = pd.DataFrame()

    # Concatenate the specified groups into the DataFrame
    for i in range(group_range[0], group_range[1]):
        table_df = tables[i].df
        table_df.columns = table_df.iloc[0]  # Set the first row as the header
        table_df = table_df[1:]  # Remove the first row
        subject_df = pd.concat([subject_df, table_df], axis=0, ignore_index=True)

    # Convert columns to numeric where possible
    subject_df = subject_df.apply(pd.to_numeric, errors='ignore')

    # Filter the DataFrame and calculate the total marks
    total_marks = subject_df[subject_df[filter_subject].astype(float) >= filter_marks][[main_subject]].astype(float).sum()[main_subject]
    
    return total_marks

# ====================================================================================================================

def pdf_to_markdown(pdf_filepath):
    """
    Converts the content of a PDF file to Markdown format and formats it using Prettier version 3.4.2.

    This function automates the extraction of text from a PDF document, converts the extracted content into Markdown, and ensures consistent formatting by utilizing Prettier 3.4.2. The process involves:
    1. Extracting text from the specified PDF file.
    2. Converting the extracted text into Markdown syntax.
    3. Formatting the Markdown content using Prettier version 3.4.2 to maintain consistency and readability.

    Args:
        pdf_filepath (str): The file path to the PDF document that needs to be converted.

    Returns:
        str: The content of the PDF converted into formatted Markdown.
    """

    md_text = pymupdf4llm.to_markdown(pdf_filepath)
    with open("q-pdf-to-markdown.md", "w") as f:
        f.write(md_text)

    prompt = f"""
    Please format the provided Markdown content to enhance its readability by incorporating the following elements:

    - **Headings:** Use `#` for H1, `##` for H2, and `###` for H3 headings appropriately.
    - **Block Quotes:** Apply `>` to format block quotes.
    - **Bullet Lists:** Ensure existing bullet lists are properly formatted.
    - **Tables:** Convert sequences of lines without bullet points into tables using the `|` character, where appropriate.
    - **Code Blocks:** Enclose code snippets within triple backticks (```) to create fenced code blocks.

    **Important:** Do not change, add, or remove any words; maintain the original order of the text. Ensure that the final formatted Markdown includes at least one instance of each of the following elements: H1 heading, H2 heading, H3 heading, block quote, table, and fenced code block.

    Here is the content to format:

    {md_text}

    Provide only the formatted Markdown output without altering the original text.
    """

    response = chat_completion(prompt)
    return response

# ====================================================================================================================

if __name__ == "__main__":
    print("=================Q1====================")
    page_number = 30
    print(get_ducks_sum(page_number))

    print("=================Q2====================")
    movies = fetch_imdb_movies(2,6)
    print(movies)

    print("=================Q3====================")
    print(country_outline_api_endpoint())

    print("=================Q4====================")
    city = "Osaka"
    print(get_forecast_description(city))

    print("=================Q5====================")
    country = "India"
    city = "Ahmedabad"
    print(get_maximum_latitude(country, city))

    print("=================Q6====================")
    keyword = "OpenAI"
    points = 86
    print(fetch_most_recent_link(keyword, points))

    print("=================Q7====================")
    max_date_time = "2025-03-26T11:35:54Z"
    latest_datetime = get_most_recent_valid_user("Bangalore", 110, max_date_time)
    print(latest_datetime)

    print("=================Q8====================")
    print(create_github_action_workflow("daniel.putta@gramener.com"))

    print("=================Q9====================")
    file = "test_data/q-extract-tables-from-pdf.pdf"
    group_range_str = "16-45"
    filter_marks = 27
    main_subject = 'Maths'  #'Physics'
    filter_subject = 'Maths'   #'Economics'
    total_marks = calculate_total_marks(file, group_range_str, filter_marks, main_subject, filter_subject)
    print(total_marks)

    print("=================Q10====================")
    print(pdf_to_markdown("test_data/q-pdf-to-markdown.pdf"))