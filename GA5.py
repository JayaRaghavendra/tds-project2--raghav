import pandas as pd
import json
import gzip
import re
from datetime import datetime
from collections import defaultdict
import os
import numpy as np
import yt_dlp
import subprocess
import base64
import requests
from metaphone import doublemetaphone
from rapidfuzz import fuzz
from dotenv import load_dotenv
from PIL import Image
import io
import time

load_dotenv()  

# ====================================================================================================================

def standardize_country(country_abbrev):
    country_mapping = {
        "USA": ["USA","US","U.S.A","United States"],
        "U.K": ["U.K","UK","United Kingdom"],
        "Fra": ["Fra","FR","France"],
        "Bra": ["Bra","BR","Brazil"],
        "Ind": ["Ind","IN","India"],
        "U.A.E":["U.A.E","United Arab Emirates","UAE","AE"]
    }

    for key, value in country_mapping.items():
        if country_abbrev.lower() in [i.lower() for i in value]:
            return key
        else:
            continue
    
    return country_abbrev


def clean_and_calculate_margin(file_path: str, target_product: str, target_country: str, end_date: str) -> float:
    """
    Cleans a messy Excel file of sales transaction records and calculates the total margin for filtered transactions.

    The Excel file contains 1,000 transaction records with the following challenges:
      - Customer Name: Contains leading/trailing spaces.
      - Country: Inconsistent representations (e.g., "USA" vs. "US", "UK" vs. "U.K", "Fra" for France, etc.).
      - Date: Mixed formats (e.g., "MM-DD-YYYY", "YYYY/MM/DD", etc.).
      - Product: Includes a product name and a random code (e.g., "Theta/5x01vd"); only the product name (before the slash) is relevant.
      - Sales and Cost: Contain extra spaces and the currency string ("USD"). If the Cost field is missing, it should be treated as 50% of the Sales value.
      - TransactionID: Inconsistently spaced four-digit numbers.

    This function performs the following steps:
      1. Reads the Excel file from the provided file path.
      2. Cleans and standardizes the data:
         - Trims extra spaces from the Customer Name and Country fields.
         - Normalizes the Country field to a standard format (e.g., "AE" for United Arab Emirates) by mapping inconsistent representations.
         - Standardizes Date fields to a consistent format (e.g., ISO 8601).
         - Extracts the product name from the Product field (i.e., the part before the slash).
         - Cleans the Sales and Cost fields by removing the "USD" text and extra spaces, converting them to numerical values, and handling missing Cost values as 50% of Sales.
      3. Filters transactions to include only those:
         - With a Date up to and including the specified end_date (e.g., "Thu Dec 01 2022 15:09:28 GMT+0530 (India Standard Time)").
         - Matching the target_product (after extracting the product name).
         - From the target_country (after normalization).
      4. Aggregates the total Sales and total Cost for the filtered transactions and calculates the total margin as:
            
             Total Margin = Total Sales - Total Cost

    Parameters:
    -----------
    file_path : str
        The file path to the Excel file containing the sales transaction records.
    target_product : str
        The product name to filter transactions (e.g., "Epsilon").
    target_country : str
        The target country (e.g., "AE") for filtering transactions after standardizing inconsistent representations.
    end_date : str
        The end date (inclusive) for filtering transactions. The date must be in a ISO 8601 format (e.g., 2022-12-01T15:09:28+05:30)".

    Returns:
    --------
    float
        The total margin for the filtered transactions, calculated as the difference between total Sales and total Cost.
    """

    target_country = standardize_country(target_country)

    # Step 1: Load the Excel file
    df = pd.read_excel(file_path, dtype=str)

    # Step 2: Clean and normalize fields

    ## Trim leading/trailing spaces in all string columns
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    ## Standardize country names
    df["Country"] = df["Country"].apply(lambda x: standardize_country(x))
    df["Country"] = df["Country"].str.lower()

    ## Extract product name (before the slash)
    df["Product"] = df["Product/Code"].apply(lambda x: x.split("/")[0] if isinstance(x, str) else x)

    ## Standardize dates (convert to consistent format)
    df["Date"] = pd.to_datetime(df["Date"],format='mixed')

    if end_date.endswith("Z"):
        end_date = end_date.replace("Z", "+00:00")

    ## Convert the end_date parameter to a datetime object
    filter_date = pd.to_datetime(end_date).to_datetime64()
    
    ## Convert TransactionID to proper format (remove spaces, ensure it's an integer)
    df["TransactionID"] = df["TransactionID"].str.replace(" ", "").astype(str)

    ## Remove "USD" and convert Sales & Cost to numeric values
    df["Sales"] = df["Sales"].str.replace("USD", "").str.strip().astype(float)
    df["Cost"] = df["Cost"].str.replace("USD", "").str.strip()
    df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")

    ## Handle missing Cost values (assume Cost = 50% of Sales)
    df.loc[:, "Cost"] = df["Cost"].fillna(df["Sales"] * 0.5)

    # Step 3: Apply Filters

    ## Filter for target country, target product, and transactions before the given date
    filtered_df = df[
        (df["Country"] == target_country.lower()) &
        (df["Product"] == target_product) &
        (df["Date"] <= filter_date)
    ]

    # Step 4: Compute Total Sales, Total Cost, and Margin

    total_sales = filtered_df["Sales"].sum()
    total_cost = filtered_df["Cost"].sum()

    if total_sales == 0:
        return 0  # Avoid division by zero

    total_margin = (total_sales - total_cost) / total_sales  # Margin %

    return round(total_margin, 4)  # Return the margin percentage rounded to 2 decimal places

# ====================================================================================================================

def count_unique_students(file_path: str) -> int:
    """
    Reads a text file, extracts student IDs (numbers after 'Marks'), removes duplicates, and 
    returns the count of unique student IDs.

    Parameters:
        file_path (str): Path to the text file containing student records.

    Returns:
        int: The number of unique student IDs in the file.
    """
    unique_student_ids = set()
    # Read the file and extract student IDs
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # Remove extra spaces and newlines
            if "-" in line and "Marks" in line:  # Ensure line contains ID & Marks
                parts = line.split("-")  # Split at the hyphen
                student_id_part = parts[-1].split("Marks")[0]  # Extract text before "Marks"
                student_id = student_id_part.strip()  # Remove leading/trailing spaces
                cleaned_id = re.sub(r"[^A-Za-z0-9]+$", "", student_id)  # Remove trailing special characters
                #cleaned_id = clean_student_id(student_id_part)  # Clean the extracted ID
                unique_student_ids.add(cleaned_id)  # Add to set

    return len(unique_student_ids)  # Return count of unique students

# ====================================================================================================================

def count_successful_get_requests(log_file_path, start_time, end_time, language, day):
    """
    Counts the number of successful GET requests for a specific language section within a given time frame on a specified day from an Apache log file.

    Parameters:
    log_file_path (str): Path to the Apache log file.
    start_time (str): Start time in 'HH:MM' format (24-hour clock) representing the beginning of the time window.
    end_time (str): End time in 'HH:MM' format (24-hour clock) representing the end of the time window.
    language (str): Language section to filter the requests (e.g., 'telugu' for URLs under '/telugu/').
    day (str): Day of the week to filter the requests (e.g., 'Sunday').

    Returns:
    int: The count of successful GET requests matching the specified criteria.

    Notes:
    - Assumes log entries are in the combined log format and timestamps are in GMT-0500 timezone.
    - A successful request is defined as one with a status code in the range 200-299.
    - The function utilizes the 'apachelogs' library for parsing log files. Ensure it is installed before use.
    - Time comparisons are inclusive of the start time and exclusive of the end time.
    - The function reads the log file line by line, which is memory efficient for large files.
    """

    # Initialize counter
    successful_requests = 0
    language="/"+language+"/"
    count=0
    ls=[]
    # Read and process the gzipped log file
    with gzip.open(log_file_path, "rt", encoding="utf-8") as file:
        for line in file:
            #print(line)
            match = re.search(r'HTTP/\d\.\d"\s+(\d{3})', line)
            status_code = int(match.group(1))
            #print(status_code)
            
            if("GET" in line and language in line and (200 <= status_code < 300)):
                start=line.find("[")
                end=line.find("]")
                date=line[start+1:end].split(" ")[0]
                ls.append(date)
    df=pd.DataFrame(ls,columns=["date"])

    # Convert to datetime
    df["datetime"] = df["date"].apply(lambda x: datetime.strptime(x, "%d/%b/%Y:%H:%M:%S"))

    # Extract day name and time
    df["day"] = df["datetime"].dt.strftime("%A")       # e.g., "Friday"
    df["time"] = df["datetime"].dt.strftime("%H:%M:%S")  # e.g., "04:31:14"
    
    # Filter rows where hour is between 5 and 10 (inclusive of 5, exclusive of 11)
    df_filtered = df[(df["datetime"].dt.hour >= int(start_time.split(":")[0])) & (df["datetime"].dt.hour < int(end_time.split(":")[0]))&(df["day"]==day)]
    return df_filtered.shape[0]

# ====================================================================================================================

def parse_apache_log_line(line):
    """
    Parses a single Apache log entry and extracts relevant fields.
    """
    log_pattern = re.compile(
        r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d+) (?P<size>\d+|-) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)" (?P<vhost>\S+) (?P<server>[\d\.]+)'
    )

    match = log_pattern.match(line)
    if match:
        log_data = match.groupdict()
        log_data["size"] = int(log_data["size"]) if log_data["size"].isdigit() else 0
        log_data["status"] = int(log_data["status"])  # Convert status to integer
        return log_data

    return None

def process_apache_log(log_file_path, page_section, date):
    """
    Analyze an Apache log file to determine the total number of bytes downloaded by the top IP address
    for a specific page section on a given date, considering only successful requests.

    Parameters:
    log_file_path (str): The file path to the GZipped Apache log file.
    page_section (str): The URL path prefix to filter requests (e.g., '/telugump3/').
    date (str): The date to filter requests in 'YYYY-MM-DD' format (e.g., '2024-05-13').

    Returns:
    tuple: The total number of bytes (int) downloaded by the top IP address by download volume.
    """
    total_data_by_ip = defaultdict(int)

    with gzip.open(log_file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            log_entry = parse_apache_log_line(line)
            if log_entry:
                # Convert log timestamp to datetime object
                log_timestamp = log_entry["timestamp"]
                log_date = datetime.strptime(log_timestamp.split(':')[0], "%d/%b/%Y").date()

                # Check if the request is for the specified page_section, the date matches, and the status code indicates success
                if (log_date == datetime.strptime(date, "%Y-%m-%d").date() and
                    log_entry["url"].startswith(page_section) and
                    200 <= log_entry["status"] < 300):
                    total_data_by_ip[log_entry["ip"]] += log_entry["size"]

    # Find the top data-consuming IP
    if total_data_by_ip:
        top_ip = max(total_data_by_ip, key=total_data_by_ip.get)
        top_bytes = total_data_by_ip[top_ip]
        return top_bytes
    else:
        return 0

# ====================================================================================================================

def process_sales_data(json_file_path, city, product, min_sales):
    """
    Processes a JSON dataset of sales entries to determine the total number of units sold for a given product
    in a specified city, after filtering transactions based on a minimum units sold threshold and grouping mis-spelt
    city names via phonetic clustering.

    The input JSON file contains sales records with these fields:
      - city: The city where the sale was made (city names may be mis-spelt, e.g., "Tokio" for "Tokyo").
      - product: The product sold (consistently spelled).
      - sales: The number of units sold.

    The function performs the following steps:
      1. Applies a phonetic clustering algorithm to group together variants of city names.
      2. Filters the records to include only those where:
           - The product matches the specified product.
           - The number of units sold is at least the specified minimum.
      3. Aggregates the total units sold for the target city (after clustering).

    Parameters:
    -----------
    json_file_path : str
        The file path to the JSON file containing sales entries.
    city : str
        The target city to filter and aggregate sales (e.g., "London").
    product : str
        The product to filter on (e.g., "Pizza").
    min_sales : int
        The minimum number of units sold in a transaction for it to be considered.

    Returns:
    --------
    int
        The total number of units sold for the specified product in the target city, considering only transactions
        that meet or exceed the minimum units sold threshold.
    """
    
    # Load JSON data into a DataFrame
    df = pd.read_json(json_file_path)
    
    # Convert relevant string columns to lowercase for consistency
    df["city"] = df["city"].str.lower()
    df["product"] = df["product"].str.lower()
    
    # Also convert filter inputs to lowercase
    city = city.lower()
    product = product.lower()
    
    # Compute primary phonetic code for each city using Double Metaphone
    df["phonetic_code"] = df["city"].apply(lambda x: doublemetaphone(x)[0])
    
    # Automated clustering of similar phonetic codes based on fuzzy similarity
    clusters = []
    threshold = 80  # similarity threshold
    
    for idx, row in df.iterrows():
        code = row["phonetic_code"]
        added = False
        for cluster in clusters:
            rep_code = cluster["rep_code"]
            similarity = fuzz.ratio(code, rep_code)
            if similarity >= threshold:
                cluster["indices"].append(idx)
                added = True
                break
        if not added:
            clusters.append({"rep_code": code, "indices": [idx]})
    
    # Function to compute the mode of a list of names
    def get_mode_name(names):
        mode_series = pd.Series(names).mode()
        return mode_series.iloc[0] if not mode_series.empty else names[0]
    
    # Build a mapping from DataFrame index to canonical city name
    cluster_mapping = {}
    for cluster in clusters:
        indices = cluster["indices"]
        city_names = df.loc[indices, "city"].tolist()
        canonical = get_mode_name(city_names)
        for i in indices:
            cluster_mapping[i] = canonical
    df["canonical_city"] = df.index.map(cluster_mapping)
    
    # Function to convert an input city name to its canonical form using the clusters
    def get_canonical_city(input_city):
        input_code = doublemetaphone(input_city)[0]
        best_match = None
        best_score = -1
        for cluster in clusters:
            rep_code = cluster["rep_code"]
            score = fuzz.ratio(input_code, rep_code)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = get_mode_name(df.loc[cluster["indices"], "city"].tolist())
        return best_match if best_match is not None else input_city

    # Convert the input city filter to its canonical form
    canonical_filter = get_canonical_city(city)
    
    # Filter records by canonical city, product, and minimum sales
    filtered_df = df[
        (df["canonical_city"] == canonical_filter) &
        (df["product"] == product) &
        (df["sales"] >= min_sales)
    ]
    
    # Aggregate sales
    aggregated_sales = filtered_df["sales"].sum()
    
    return aggregated_sales

# ====================================================================================================================

def calculate_total_sales_jsonl(jsonl_file_path: str) -> float:
    """
    Calculate the total sales from a JSONL file containing sales data.

    This function reads a JSONL file where each line is a JSON object representing a sales record.
    It extracts the 'sales' value from each record, handles missing or malformed entries gracefully,
    and computes the aggregate total of all sales values.

    Parameters:
    jsonl_file_path (str): The file path to the JSONL file containing sales data.

    Returns:
    float: The total sales value computed from all valid records in the file.
    """
    total_sales = 0.0

    # Open the JSONL file and read it line by line
    with open(jsonl_file_path, "r", encoding="utf-8") as file:
        for line in file:
            #print(line)
            ind=line.find("sales")
            total_sales=total_sales+float((line[ind:].split(":")[1].split(",")[0]))

    return total_sales

# ====================================================================================================================

def count_key_occurrences(json_file_path, target_key):
    """
    Count the number of times a specific key appears in a nested JSON structure.

    This function reads a JSON file, parses its content, and recursively traverses
    the JSON structure to count occurrences of the specified key.

    Parameters:
    json_file_path (str): The file path to the JSON file.
    target_key (str): The key to count within the JSON structure.

    Returns:
    int: The total number of times the target key appears in the JSON structure.
    """

    # Read the JSON file
    with open(json_file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)  # Load JSON once

    def recursive_count(data, key):
        """Helper function to traverse JSON recursively."""
        count = 0
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    count += 1  # Increment if the key matches
                count += recursive_count(v, key)  # Recursive call
        elif isinstance(data, list):
            for item in data:
                count += recursive_count(item, key)  # Traverse lists
        return count

    # Call the helper function to start recursion
    return recursive_count(json_data, target_key)

# ====================================================================================================================

def generate_duckdb_query(min_timestamp: str, min_useful_stars: int) -> str:
    """
    Generates a DuckDB SQL query string to extract post IDs for high-impact posts.

    This function returns a SQL query that:
      - Filters posts with a timestamp greater than or equal to the specified min_timestamp.
      - Joins the posts with the comments table to ensure that at least one comment has more than
        the specified number of useful stars (min_useful_stars).
      - Extracts the distinct post_id values from the resulting posts.
      - Sorts the post IDs in ascending order.

    The resulting query is intended for execution in DuckDB and returns a table with a single column,
    'post_id', containing the sorted list of qualifying post IDs.

    Parameters:
    -----------
    min_timestamp : str
        The minimum timestamp to filter posts. The timestamp should be in ISO 8601 UTC format, e.g.,
        "2025-01-05T18:02:26.045Z".
    min_useful_stars : int
        The threshold for the minimum number of useful stars a comment must have.

    Returns:
    --------
    str
        A DuckDB SQL query string that, when executed, returns the sorted post IDs meeting the criteria.
    """

    query = f"""
    SELECT post_id
    FROM social_media
    WHERE timestamp >= '{min_timestamp}'
    AND EXISTS (
        SELECT 1
        FROM UNNEST(comments) AS comment
        WHERE CAST(comment.stars->>'useful' AS INTEGER) > {min_useful_stars}
    )
    ORDER BY post_id ASC;
    """
    return query

# ====================================================================================================================

def extract_and_transcribe(start_time, stop_time):
    """
    Generates a transcript for a specific segment of a YouTube video.

    This function accesses the provided YouTube URL, extracts the audio segment between the given 
    start_time and stop_time (in seconds), and uses automated speech-to-text processing to produce an 
    accurate transcript of the spoken content in that segment. The transcription aims to capture all 
    spoken dialogue and descriptive narration accurately, with appropriate punctuation and paragraph 
    breaks, while excluding any extraneous noise or background commentary.

    Parameters:
    -----------
    start_time : float
        The starting time (in seconds) of the segment to be transcribed (e.g., 108.8).
    stop_time : float
        The ending time (in seconds) of the segment to be transcribed (e.g., 282.6).

    Returns:
    --------
    str
        The transcript text of the video segment between start_time and stop_time.
    """

    youtube_url = "https://youtu.be/NRntuOJu4ok"
    MP3_FILE = "downloaded_audio.mp3"
    SEGMENT_FILE = "audio_segment.mp3"
    DURATION = stop_time - start_time

    # Step 1: Download the audio from YouTube using yt-dlp
    # Define a custom logger that suppresses all output
    class SilentLogger:
        def debug(self, msg): pass
        def info(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): pass

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": MP3_FILE,
        "quiet": True,
        "no_warnings": True,
        "logger": SilentLogger(),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Step 2: Trim the MP3 file using FFmpeg via subprocess
    # Specify the absolute path to your FFmpeg binary.
    ffmpeg_path = os.path.join(os.getcwd(),"ffmpeg-7.0.2-amd64-static/ffmpeg")

    # Build the FFmpeg command:
    # -i: input file
    # -ss: start time (in seconds)
    # -t: duration (in seconds)
    # -acodec copy: copy the audio codec without re-encoding (if this causes sync issues, remove it to force re-encoding)
    # -y: overwrite output file without asking
    cmd = [
        ffmpeg_path,
        "-i", MP3_FILE,
        "-ss", str(start_time),
        "-t", str(DURATION),
        "-acodec", "libmp3lame",  # re-encode to MP3
        SEGMENT_FILE,
        "-y"
    ]

    # Run the command and check for errors
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step 3: Read and encode the trimmed MP3 segment in base64
    with open(SEGMENT_FILE, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode("utf-8")

    # Construct the payload for the transcription API
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "audio/mp3",
                            "data": audio_data
                        }
                    },
                    {"text": "Transcribe this"}
                ]
            }
        ]
    }

    # API URL and headers
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:streamGenerateContent?alt=sse"
    headers = {
        "X-Goog-API-Key": os.getenv("GEMINI_API_KEY"),
        "Content-Type": "application/json"
    }

    # Step 4: Make the request to the Gemini API and print the transcription output
    audio_transcription = ""
    retries = 3  # Maximum number of retries
    delay = 1  # Initial delay in seconds

    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            for line in response.iter_lines():
                if line:
                    output = line.decode("utf-8")
                    output = json.loads(output[6:])
                    audio_transcription += output["candidates"][0]["content"]["parts"][0]["text"]
            return audio_transcription  # Success, return the transcription

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 503:
                error_msg = e.response.text
                print(f"Attempt {attempt + 1} failed with 503. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Attempt {attempt + 1} failed with error: {e}")
                return audio_transcription # return with whatever transcription was gathered so far.
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with exception: {e}")
            return audio_transcription # return with whatever transcription was gathered so far.

    print("Maximum retries reached. Unable to get transcription.")
    return error_msg # return with whatever transcription was gathered so far.

# ====================================================================================================================

def reconstruct_image(scrambled_image_path: str, mapping: list) -> str:
    """
    Reconstructs an image from its scrambled pieces using a specified mapping.

    This function takes a scrambled image and reassembles it into its original form based on the provided mapping of piece positions.

    Args:
        scrambled_image_path (str): The file path to the scrambled image.
        piece_mappings (list of tuples): A list of tuples, each containing four integers:
            (original_row, original_col, scrambled_row, scrambled_col).
            These values represent the original and scrambled positions of each piece in the format:
            (Original Row, Original Column, Scrambled Row, Scrambled Column).
    """

    grid_size = 5  # 5x5 grid
    piece_size = 100  # Each piece is 100x100 pixels (since 500/5 = 100)
    
    # Load the scrambled image
    scrambled_image = Image.open(scrambled_image_path)
    
    # Create a blank image to reconstruct the original
    reconstructed_image = Image.new('RGB', (500, 500))
    
    for original_row, original_col, scrambled_row, scrambled_col in mapping:
        # Compute the coordinates of the scrambled piece
        scrambled_x = scrambled_col * piece_size
        scrambled_y = scrambled_row * piece_size
        
        # Extract the scrambled piece
        piece = scrambled_image.crop((scrambled_x, scrambled_y, scrambled_x + piece_size, scrambled_y + piece_size))
        
        # Compute the coordinates where the piece should go in the original image
        original_x = original_col * piece_size
        original_y = original_row * piece_size
        
        # Paste the piece in the correct position
        reconstructed_image.paste(piece, (original_x, original_y))
    
    # Write the reconstructed image to an in-memory bytes buffer
    buffered = io.BytesIO()
    reconstructed_image.save(buffered, format="WEBP")
    
    # Get the byte data from the buffer and encode it as base64
    img_bytes = buffered.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/webp;base64,{img_base64}"

# ====================================================================================================================

if __name__ == "__main__":
    print("=================Q1===================")
    file_path = "test_data/q-clean-up-excel-sales-data.xlsx"  # Replace with actual file path
    target_product = "Epsilon"
    target_country = "UAE"
    end_date = "2022-12-01T15:09:28+05:30"
    margin = clean_and_calculate_margin(file_path, target_product, target_country, end_date)
    print(margin)

    print("=================Q2===================")
    file_path = "test_data/q-clean-up-student-marks.txt"  # Replace with actual file path
    unique_student_count = count_unique_students(file_path)
    print(unique_student_count)

    print("=================Q3===================")
    log_file_path = "test_data/s-anand.net-May-2024.gz"  # Path to your gzipped Apache log file
    start_time ='12:00'
    end_time ='21:00'
    language='telugu'
    day='Sunday'
    successful_get_requests = count_successful_get_requests(log_file_path,start_time,end_time,language,day)
    print(successful_get_requests)

    print("=================Q4===================")
    file_path = "test_data/s-anand.net-May-2024.gz"  # Replace with the actual path of your GZipped log file
    date = "2024-05-13"
    page_section="/telugump3/"
    top_bytes = process_apache_log(file_path,page_section,date)
    print(top_bytes)

    print("=================Q5===================")
    json_file = "test_data/q-clean-up-sales-data.json"
    city_input = "London"
    product_input = "Pizza"
    min_sales_input = 102
    total_sales = process_sales_data(json_file, city_input, product_input, min_sales_input)
    print(total_sales)

    print("=================Q6===================")
    json_file_path = "test_data/q-parse-partial-json.jsonl"  # Replace with actual file path
    total_sales = calculate_total_sales_jsonl(json_file_path)
    print(total_sales)

    print("=================Q7===================")
    file_path = "test_data/q-extract-nested-json-keys.json"  # Update with actual file name
    target_key = "HMZQ"
    occurrences = count_key_occurrences(file_path, target_key)
    print(occurrences)

    print("=================Q8===================")
    min_time = "2025-01-05T18:02:26.045Z"
    min_useful_stars = 4
    duckdb_query = generate_duckdb_query(min_time, min_useful_stars)
    print(duckdb_query)

    print("=================Q9===================")
    start = 108.8
    stop = 282.6
    transcript = extract_and_transcribe(start, stop)
    print(transcript)

    print("=================Q10===================")
    mapping_data = [
        (2,1,0,0), (1,1,0,1), (4,1,0,2), (0,3,0,3), (0,1,0,4),
        (1,4,1,0), (2,0,1,1), (2,4,1,2), (4,2,1,3), (2,2,1,4),
        (0,0,2,0), (3,2,2,1), (4,3,2,2), (3,0,2,3), (3,4,2,4),
        (1,0,3,0), (2,3,3,1), (3,3,3,2), (4,4,3,3), (0,2,3,4),
        (3,1,4,0), (1,2,4,1), (1,3,4,2), (0,4,4,3), (4,0,4,4)
    ]
    print(reconstruct_image("GA5_10.webp", mapping_data))