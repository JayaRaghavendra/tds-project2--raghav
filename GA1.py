import subprocess
import json
import requests
import os
import re
import shutil
from bs4 import BeautifulSoup
import zipfile
import pandas as pd
import csv
import io
from github import Github
from dotenv import load_dotenv
from llm_utils import *

load_dotenv()

def run_code_status():
    """
    Executes the 'code -s' command in the terminal (or Command Prompt) to retrieve the status of Visual Studio Code.

    Returns:
        str: The output of executing the "code --status in terminal"
    """

    filepath = "GA1_1.txt"
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# ====================================================================================================================


def run_uv(email_address):
    """
    Runs an HTTP request to httpbin.org with the given email address.

    Args:
        email_address: The email address to include in the request.

    Returns:
        A tuple containing (return_code, json_output, error_message).
        return_code: The exit code of the command (integer).
        json_output: The parsed JSON output (dictionary) or None.
        error_message: An error message (string) or None.
    """
    command_list = ["/usr/local/bin/uv", "run", "--with", "httpie", "--", "http", "GET", "https://httpbin.org/get", f"email=={email_address}"]

    try:
        process = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=False,
        )
        stdout = process.stdout.strip() if process.stdout else ""
        stderr = process.stderr.strip() if process.stderr else ""
        return_code = process.returncode

        if return_code == 0:
            try:
                return stdout
            except json.JSONDecodeError:
                return None
        else:
            return None

    except Exception as e:
        return None

# ====================================================================================================================

def run_prettier(readme_file_path):
    """
    Formats the specified README file using Prettier and calculates its SHA-256 checksum.

    This function executes the command:
        "npx -y prettier@3.4.2 <readme_file_path> | sha256sum"
    using the system shell. It:
    1. Runs Prettier (version 3.4.2) on the given README file.
    2. Formats the file according to Prettier's rules.
    3. Computes and returns the SHA-256 checksum of the formatted output.

    Args:
        readme_file_path (str): The file path of the README file to format.

    Returns:
        - stdout (str): The SHA-256 checksum of the formatted content.
    """

    command_string = f"npx -y prettier@3.4.2 {readme_file_path} | sha256sum"

    try:
        process = subprocess.run(
            command_string,
            capture_output=True,
            text=True,
            check=False,
            shell=True,  # Enable shell interpretation
        )
        stdout = process.stdout.strip() if process.stdout else ""
        stderr = process.stderr.strip() if process.stderr else ""
        return_code = process.returncode

        return stdout
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# ====================================================================================================================

def calculate_formula_in_google_sheet(formula):
    """
    Puts a formula in a google sheet at A1 cell, computes in B1, and returns the result from B1.

    Args:
        formula: The formula string.

    Returns:
        The computed result, or None if an error occurs.
    """

    # The URL of your Google Apps Script web app.
    web_app_url = "https://script.google.com/macros/s/AKfycbzqSnAvZWmFgIrqofWolaflgaeiRz1Vi6toM1-EXX5fDCF6SffZMwV_hvs0i9VHLVs5/exec"

    try:
        data = {"formula": formula}
        headers = {"Content-Type": "application/json"}
        response = requests.post(web_app_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        result = response.json().get("result")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None

# ====================================================================================================================

def calculate_formula_in_excel_365_sheet(formula):
    """
    Evaluates a given Excel formula and returns its output.

    This function inserts the provided formula into an Excel sheet, calculates its result, 
    and retrieves the output. It is designed for use with Office 365, where dynamic formulas 
    are supported.

    Args:
        formula (str): The Excel formula to be evaluated as a string.

    Returns:
        str: The output of the evaluated formula.
    """

    # Extract arrays inside {}
    arrays = re.findall(r"\{([^}]*)\}", formula)
    array1 = list(map(int, arrays[0].split(','))) if len(arrays) > 0 else []
    array2 = list(map(int, arrays[1].split(','))) if len(arrays) > 1 else []

    # Extract standalone numbers (not inside arrays)
    numbers = [int(num) for num in re.findall(r"[-]?\d+", formula)]
    num3, num4 = numbers[-2:]  # Last two numbers (for TAKE function)

    # SORTBY: Sort array1 based on values in array2
    sorted_array = [x for _, x in sorted(zip(array2, array1))]

    # TAKE: Take the first 'num4' elements after sorting
    if num4 > 0:
        taken_values = sorted_array[:num4]
    elif num4 < 0:
        taken_values = sorted_array[num4:]
    else:
        taken_values = []

    # SUM: Compute sum of the taken values
    result = str(sum(taken_values))

    return result

# ====================================================================================================================

def extract_hidden_input_value(html_path):
    """
    Extracts the value of a hidden input field from an HTML file.

    This function parses the given HTML file to locate the first hidden input field 
    and retrieves its 'value' attribute.

    Args:
        html_path (str): The path to the HTML file containing the hidden input field.

    Returns:
        str: The value of the hidden input field.
    """

    # Load the HTML file
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the hidden input element with type="hidden" and disabled attribute
    hidden_input = soup.find("input", {"type": "hidden", "disabled": True})

    # Get the value attribute
    input_value = hidden_input["value"] if hidden_input else None

    return input_value

# ====================================================================================================================

def count_days_in_range(start_date_str, end_date_str, target_day_name):
    """
    Counts the number of occurrences of a specific day of the week within a given date range.

    Args:
        start_date_str: The start date in 'YYYY-MM-DD' format.
        end_date_str: The end date in 'YYYY-MM-DD' format.
        target_day_name: The name of the day of the week (e.g., "Monday", "Wednesday").

    Returns:
        The number of occurrences of the target day within the date range.
    """
    import datetime
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        target_day_index = day_names.index(target_day_name)

        count = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == target_day_index:
                count += 1
            current_date += datetime.timedelta(days=1)

        return count

    except ValueError:
        return "Invalid date format or day name."

# ====================================================================================================================

def get_answer_from_csv(zip_file_path: str) -> str:
    """
    Extracts and returns the value from the "answer" column in the extract.csv file 
    inside a given ZIP archive.

    This function:
    1. Extracts the ZIP file.
    2. Searches for "extract.csv".
    3. Reads the CSV file and retrieves the value from the "answer" column.

    Args:
        zip_file_path (str): The file path to the ZIP archive.

    Returns:
        str: The value in the "answer" column of extract.csv.
    """

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract all files to a temporary directory
            temp_dir = "temp_unzipped"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            zip_ref.extractall(temp_dir)

            # Find the CSV file (assuming only one CSV exists)
            csv_file_path = None
            for filename in os.listdir(temp_dir):
                if filename.lower().endswith(".csv"):
                    csv_file_path = os.path.join(temp_dir, filename)
                    break

            if csv_file_path:
                # Read the CSV using pandas
                df = pd.read_csv(csv_file_path)

                # Extract the 'answer' column
                if 'answer' in df.columns:
                    answers = df['answer'].tolist()

                    # Clean up the temporary directory
                    for filename in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, filename)
                        os.remove(file_path)
                    os.rmdir(temp_dir)

                    return answers[0]
                else:
                    print("Error: 'answer' column not found in the CSV.")
                    # Clean up the temporary directory
                    for filename in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, filename)
                        os.remove(file_path)
                    os.rmdir(temp_dir)
                    return None

            else:
                print("Error: No CSV file found in the zip archive.")
                # Clean up the temporary directory
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    os.remove(file_path)
                os.rmdir(temp_dir)
                return None

    except FileNotFoundError:
        print(f"Error: Zip file not found at {zip_file_path}")
        return None
    except zipfile.BadZipFile:
        print(f"Error: {zip_file_path} is not a valid zip file.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        # Clean up the temporary directory
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            os.remove(file_path)
        os.rmdir(temp_dir)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                os.remove(file_path)
            os.rmdir(temp_dir)
        return None

# ====================================================================================================================

def sort_json_by_age_and_name(json_string: str) -> str:
    """
    Sorts a JSON array of objects by the 'age' field in ascending order. 
    In case of a tie, sorts by the 'name' field alphabetically.

    Args:
        json_string (str): The input JSON string containing an array of objects.

    Returns:
        str: The sorted JSON array as a compact string without spaces or newlines.
    """

    try:
        data = json.loads(json_string)
        sorted_data = sorted(data, key=lambda x: (x.get("age"), x.get("name")))
        return json.dumps(sorted_data, separators=(',', ':'))
    except json.JSONDecodeError:
        return "Invalid JSON"

# ====================================================================================================================

def convert_txt_to_json_and_hash(txt_filepath: str) -> str:
    """
    Reads a text file containing key=value pairs, converts it into a single JSON object, 
    and computes its hash using the online tool at tools-in-data-science.pages.dev/jsonhash.

    This function:
    1. Reads the text file.
    2. Parses key=value pairs and converts them into a JSON object.
    3. Returns the computed hash after pasting the JSON into the tool.

    Args:
        txt_filepath (str): The file path to the text file containing key=value pairs.

    Returns:
        str: The hash generated by tools-in-data-science.pages.dev/jsonhash.
    """

    try:
        with open(txt_filepath, "r") as file:
            data = file.readlines()
            data = ['"'+line.replace("\n","").replace('=','\":\"')+'"' for line in data]
            output = ','.join(data)
            output = '{'+output+'}'

        command = ["node", "cli.mjs", output]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout
        else:
            return None

    except FileNotFoundError:
        print(f"Error: File not found at {txt_filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# ====================================================================================================================

def sum_data_values_of_divs(html_path: str) -> int:
    """
    Parses an HTML file, finds all <div> elements with the class 'foo' inside a hidden element, 
    and sums their 'data-value' attributes.

    This function:
    1. Reads the HTML file.
    2. Selects all <div> elements with the class 'foo' inside a hidden element.
    3. Extracts their 'data-value' attributes and calculates the sum.

    Args:
        html_path (str): The file path to the HTML file.

    Returns:
        int: The sum of the 'data-value' attributes of the matching <div> elements.

    Raises:
        FileNotFoundError: If the specified HTML file does not exist.
        ValueError: If 'data-value' attributes are missing or not numeric.
        ImportError: If the required HTML parsing library (e.g., BeautifulSoup) is not installed.
    """

    # Load the HTML file
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the hidden div with class 'd-none' and the exact title
    hidden_element = soup.find("div", class_="d-none", title="This is the hidden element with the data-value attributes")

    # Find all 'div' elements with class 'foo' inside the hidden div
    foo_divs = hidden_element.find_all("div", class_="foo") if hidden_element else []

    # Sum the data-value attributes
    sum_value = sum(int(div.get("data-value", 0)) for div in foo_divs)

    return sum_value

# ====================================================================================================================

def sum_values_for_symbols(zip_file_path: str, target_symbols: list) -> int:
    """
    Reads and processes three differently encoded files, summing values for specific symbols 
    across all files.

    The function handles:
    - data1.csv (CP-1252 encoding, comma-separated)
    - data2.csv (UTF-8 encoding, comma-separated)
    - data3.txt (UTF-16 encoding, tab-separated)

    Each file contains two columns: 'symbol' and 'value'. This function:
    1. Reads and decodes each file appropriately based on its encoding.
    2. Filters rows where the 'symbol' column matches one of the target symbols.
    3. Sums up the corresponding 'value' column.

    Args:
        zip_file_path (str): The file path to the directory containing the three data files.
        target_symbols (list): A list of symbols to filter and sum values for.

    Returns:
        int: The total sum of values for the specified symbols.
    """

    target_symbols = set(target_symbols)  # Convert to set for efficient lookup
    total_sum = 0

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            # Process data1.csv (CP-1252)
            with zip_file.open('data1.csv') as file1:
                decoded_file1 = io.TextIOWrapper(file1, encoding='cp1252')
                reader1 = csv.reader(decoded_file1)
                for row in reader1:
                    if len(row) == 2 and row[0] in target_symbols:
                        try:
                            total_sum += int(row[1])
                        except ValueError:
                            pass

            # Process data2.csv (UTF-8)
            with zip_file.open('data2.csv') as file2:
                decoded_file2 = io.TextIOWrapper(file2, encoding='utf-8')
                reader2 = csv.reader(decoded_file2)
                for row in reader2:
                    if len(row) == 2 and row[0] in target_symbols:
                        try:
                            total_sum += int(row[1])
                        except ValueError:
                            pass

            # Process data3.txt (UTF-16)
            with zip_file.open('data3.txt') as file3:
                decoded_file3 = io.TextIOWrapper(file3, encoding='utf-16')
                reader3 = csv.reader(decoded_file3, delimiter='\t')
                for row in reader3:
                    if len(row) == 2 and row[0] in target_symbols:
                        try:
                            total_sum += int(row[1])
                        except ValueError:
                            pass

    except FileNotFoundError:
        print(f"Error: Zip file not found at {zip_file_path}")
    except KeyError as e:
        print(f"Error: File not found in zip archive: {e}")
    except zipfile.BadZipFile:
        print(f"Error: Invalid zip file: {zip_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return total_sum

# ====================================================================================================================

def create_github_repo_and_push_json(email_id: str) -> str:
    """
    Automates the process of creating a GitHub repository, committing a JSON file, 
    and pushing it to GitHub.

    This function:
    1. Creates a JSON file named 'email.json' with the structure: {"email": email_id}.
    2. Initializes a new GitHub repository (public).
    3. Commits and pushes the JSON file to the repository.
    4. Returns the raw GitHub URL of the uploaded file.

    Args:
        email_id (str): The email address to be stored in the JSON file.

    Returns:
        str: The raw GitHub URL of email.json.
    """

    new_content = json.dumps({"email": email_id}, indent=2)

    # Get token from environment variables
    token = os.getenv("ACCESS_TOKEN")
    if not token:
        raise EnvironmentError("ACCESS_TOKEN environment variable is not set.")
    
    # Hard-coded settings
    repo_name = "danielrayappa2210/TDS"  # Replace with your GitHub username and repository name
    branch = "main"
    file_path = "email.json"
    
    # Authenticate and get the repository
    g = Github(token)
    repos = g.get_user().get_repos()
    repo = g.get_repo(repo_name)
    
    # Retrieve the file to update (needed for its SHA)
    file = repo.get_contents(file_path, ref=branch)
    
    # Update the file with the new content
    commit_message = "Update index.html via Python script"
    update_response = repo.update_file(file.path, commit_message, new_content, file.sha, branch=branch)
    
    return "https://raw.githubusercontent.com/danielrayappa2210/TDS/refs/heads/main/email.json"

# ====================================================================================================================

def replace_iitm_and_compute_sha256(zip_filepath: str) -> str:
    """
    Extracts a ZIP archive, replaces all occurrences of 'IITM' (case-insensitive) with 'IIT Madras' 
    in all files, and computes the SHA-256 checksum of the concatenated file contents.

    This function:
    1. Extracts the ZIP archive into a new folder.
    2. Recursively processes all files, replacing 'IITM' (case-insensitive) with 'IIT Madras'.
    3. Preserves original line endings.
    4. Computes the SHA-256 hash of all file contents using the equivalent of `cat * | sha256sum`.

    Args:
        zip_filepath (str): The file path to the ZIP archive.

    Returns:
        str: The computed SHA-256 hash.
    """
    from datetime import datetime
    # Create a destination folder named "<zipfilename>_unzipped"
    dest_dir = os.path.splitext(os.path.basename(zip_filepath))[0] + "_unzipped"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving file timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))
    
    # Replace all occurrences of "IITM" (any case) with "IIT Madras" in every file.
    for root, _, files in os.walk(dest_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                data = f.read()
            new_data = re.sub(b'iitm', b'IIT Madras', data, flags=re.IGNORECASE)
            if new_data != data:
                with open(file_path, 'wb') as f:
                    f.write(new_data)
    
    # Run "cat * | sha256sum" in the destination folder and return its output.
    output = subprocess.check_output("cat * | sha256sum", shell=True, cwd=dest_dir, text=True).strip()
    return output

# ====================================================================================================================

def list_files_and_attributes(zip_filepath, min_size, min_date):
    """
    Processes the given ZIP file by:
      - Extracting it into a folder named "<zipfilename>_unzipped" (preserving timestamps),
      - Using 'ls -l --time-style=long-iso' to list files with their modification date and size,
      - Filtering files that are at least min_size bytes and modified on or after min_date,
      - Summing their sizes using an awk command.
    
    Args:
      zip_filepath (str): Path to the ZIP file.
      min_size (int): Minimum file size in bytes.
      min_date (str): Minimum modification date in the format "YYYY-MM-DD HH:MM" 
                      (e.g., "1999-02-01 17:40").
    
    Returns:
      str: The output of the shell command (the total size of the matching files).
    """
    from datetime import datetime

    # Create destination folder "<zipfilename>_unzipped"
    dest_dir = os.path.splitext(os.path.basename(zip_filepath))[0] + "_unzipped"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))
    
    # Construct the shell command:
    # Use ls with --time-style=long-iso to get ISO-like date format.
    # awk filters files with size >= min_size and modification date/time >= min_date, then sums sizes.
    cmd = f"""ls -l --time-style=long-iso | awk '$5>={min_size} && ($6" "$7)>= "{min_date}" {{sum+=$5}} END {{print sum}}'"""
    
    # Run the shell command in the destination folder and return its output.
    output = subprocess.check_output(cmd, shell=True, cwd=dest_dir, text=True).strip()
    return output

# ====================================================================================================================

def move_rename_files(zip_filepath):
    """
    Processes the given ZIP file by:
      - Extracting it into a folder named "<zipfilename>_unzipped" while preserving file timestamps,
      - Moving all files (recursively) from the extracted folder into a new empty folder ("flat"),
      - Renaming all files in the flat folder by replacing each digit with the next digit 
        (with 9 wrapping to 0; e.g., a1b9c.txt becomes a2b0c.txt),
      - Running the shell command "grep . * | LC_ALL=C sort | sha256sum" in that folder,
      - Returning the output of the shell command.
    
    Args:
      zip_filepath (str): Path to the ZIP file.
    
    Returns:
      str: The output of the shell command.
    """
    from datetime import datetime

    # Determine destination folder based on zip filename.
    base = os.path.splitext(os.path.basename(zip_filepath))[0]
    dest_dir = base + "_unzipped"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving file timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))

    # Create an empty "flat" folder inside dest_dir.
    flat_dir = os.path.join(dest_dir, "flat")
    os.makedirs(flat_dir, exist_ok=True)

    # Move all files from the extracted directory tree into flat_dir.
    for root, dirs, files in os.walk(dest_dir):
        # Skip the flat directory itself.
        if os.path.abspath(root) == os.path.abspath(flat_dir):
            continue
        for file in files:
            source_path = os.path.join(root, file)
            dest_path = os.path.join(flat_dir, file)
            os.rename(source_path, dest_path)

    # Rename all files in flat_dir: replace each digit with the next (9 -> 0).
    def replace_digit(match):
        digit = match.group()
        return '0' if digit == '9' else str(int(digit) + 1)
    
    for file in os.listdir(flat_dir):
        old_path = os.path.join(flat_dir, file)
        new_filename = re.sub(r'\d', replace_digit, file)
        new_path = os.path.join(flat_dir, new_filename)
        if new_filename != file:
            os.rename(old_path, new_path)

    # Run the shell command and capture its output.
    output = subprocess.check_output(
        "grep . * | LC_ALL=C sort | sha256sum",
        shell=True, cwd=flat_dir, text=True
    ).strip()
    return output

# ====================================================================================================================

def compare_files(zip_filepath):
    """
    Processes the given ZIP file by:
      - Deleting the destination folder ("<zipfilename>_unzipped") if it exists,
      - Creating a new destination folder,
      - Extracting the ZIP file into that folder while preserving file timestamps,
      - Reading 'a.txt' and 'b.txt' from the folder,
      - Comparing the two files line by line to count how many lines differ,
      - Returning the count of differing lines.
    
    Args:
      zip_filepath (str): Path to the ZIP file.
    
    Returns:
      int: The number of lines that differ between a.txt and b.txt.
    """
    from datetime import datetime

    # Determine destination folder based on the zip filename.
    base = os.path.splitext(os.path.basename(zip_filepath))[0]
    dest_dir = base + "_unzipped"
    
    # If the destination folder exists, delete it.
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    # Create a new destination folder.
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))

    # Define paths for a.txt and b.txt.
    a_path = os.path.join(dest_dir, "a.txt")
    b_path = os.path.join(dest_dir, "b.txt")

    # Compare the two files line by line.
    diff_count = 0
    with open(a_path, 'r') as fa, open(b_path, 'r') as fb:
        for line_a, line_b in zip(fa, fb):
            if line_a != line_b:
                diff_count += 1

    return diff_count

# ====================================================================================================================

def generate_sql_query(question: str) -> str:
    """
    Converts a natural language question into an SQL query.

    This function takes a descriptive SQL-related question as input and returns
    the corresponding SQL query. It utilizes a prompt template to guide the
    transformation process and relies on the `chat_completion` function to
    generate the SQL query.

    Args:
        question (str): A natural language description of the desired SQL operation.

    Returns:
        str: The SQL query corresponding to the input question.
    """

    prompt_template = (
        "You are an SQL query generator. Your task is to translate a natural language description of an SQL operation "
        "into a correct SQL query. Read the input carefully and output only the SQL query as plain text—no explanations, "
        "no formatting, and no code block syntax such as triple backticks.\n\n"
        "For example:\n"
        "Input: \"Write a query to extract all the rows in table 'tickets'\"\n"
        "Output: SELECT * FROM tickets;\n\n"
        "Now, please convert the following description into an SQL query:\n"
        "{question}"
    )
    
    # Format the prompt with the provided question.
    prompt = prompt_template.format(question=question)
    
    # Get the SQL query output using your chat_completion function.
    sql_query = chat_completion(prompt)
    return sql_query

# ====================================================================================================================
# Testing the functions

if __name__ == "__main__":
    # Example usage:
    print("=================Q1====================")
    shell_output = run_code_status()
    print(shell_output)

    print("=================Q2====================")
    email_to_use = "raghavendra.bobbili@gramener.com"
    print(run_uv(email_to_use))

    print("=================Q3====================")
    print(run_prettier("./test_data/README.md"))

    print("=================Q4====================")
    formula = "=SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 0, 4), 1, 10))"
    print(calculate_formula_in_google_sheet(formula))

    print("=================Q5====================")
    formula = "=SUM(TAKE(SORTBY({10,6,10,9,11,2,7,15,11,12,6,14,2,9,2,12}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 14))"
    print(calculate_formula_in_excel_365_sheet(formula))

    print("=================Q6====================")
    print(extract_hidden_input_value("./test_data/GA1_daniel.html"))

    print("=================Q7====================")
    start_date = "1988-12-05"
    end_date = "2010-05-02"
    target_day = "Wednesday"

    result = count_days_in_range(start_date, end_date, target_day)
    print(result)

    print("=================Q8====================")
    zip_file_path = "./test_data/q-extract-csv-zip (1).zip"  # Replace with your zip file path
    print(get_answer_from_csv(zip_file_path))

    print("=================Q9====================")
    json_data = '[{"name":"Alice","age":26},{"name":"Bob","age":10},{"name":"Charlie","age":72},{"name":"David","age":56},{"name":"Emma","age":55},{"name":"Frank","age":54},{"name":"Grace","age":56},{"name":"Henry","age":18},{"name":"Ivy","age":36},{"name":"Jack","age":9},{"name":"Karen","age":95},{"name":"Liam","age":86},{"name":"Mary","age":97},{"name":"Nora","age":11},{"name":"Oscar","age":22},{"name":"Paul","age":84}]'
    sorted_json = sort_json_by_age_and_name(json_data)
    print(sorted_json)

    print("=================Q10====================")
    input_filepath = "./test_data/q-multi-cursor-json.txt"
    print(convert_txt_to_json_and_hash(input_filepath))

    print("=================Q11====================")
    print(sum_data_values_of_divs("./test_data/GA1.html"))

    print("=================Q12===================")
    zip_file_path = './test_data/q-unicode-data (1).zip'  # Replace with your zip file path.
    target_symbols = ['‡', '‹', '—']
    result = sum_values_for_symbols(zip_file_path, target_symbols)
    print(result)

    print("=================Q13===================")
    email = "daniel.putta@gramener.com"
    gh_page_url = create_github_repo_and_push_json(email)
    print(gh_page_url)

    print("=================Q14===================")
    output = replace_iitm_and_compute_sha256('./test_data/q-replace-across-files.zip')
    print(output)

    print("=================Q15===================")
    total_size = list_files_and_attributes("./test_data/q-list-files-attributes.zip", 8172, "1999-02-01 17:40")
    print(total_size)

    print("=================Q16===================")
    result = move_rename_files("./test_data/q-move-rename-files.zip")
    print(result)

    print("=================Q17===================")
    diff_lines = compare_files('./test_data/q-compare-files.zip')
    print(diff_lines)

    print("=================Q18===================")
    question = "There is a tickets table in a SQLite database that has columns type, units, and price. Each row is a customer bid for a concert ticket.\n\n| type   | units | price |\n|--------|-------|-------|\n| Silver | 38    | 1.47  |\n| SILVER | 562   | 1.98  |\n| Silver | 541   | 1.74  |\n| bronze | 224   | 0.95  |\n| BRONZE | 493   | 1.82  |\n| ...    | ...   | ...   |\n\nWhat is the total sales of all the items in the \"Gold\" ticket type? Write SQL to calculate it."
    try:
        query = generate_sql_query(question)
        print(query)
    except Exception as e:
        print("Error:", e)