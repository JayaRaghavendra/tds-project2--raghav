# GA1 function description
GA1_tools = [
    {
        "type": "function",
        "function": {
            "name": "run_code_status",
            "description": "Runs the 'code -s' command in the terminal to capture and return Visual Studio Code's full status output, including version, commit hash, build details, and environment information.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_uv",
            "description": "Sends an HTTPS GET request to https://httpbin.org/get with the URL-encoded parameter email_id (installing httpie if needed) and returns only the JSON response body.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_address": {
                        "type": "string",
                        "description": "The email address to include in the request."
                    }
                },
                "required": [
                    "email_address"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_prettier",
            "description": "Formats the README.md file using Prettier v3.4.2 via npx, pipes the output to sha256sum, and returns the resulting SHA256 hash of the formatted content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "readme_file_path": {
                        "type": "string",
                        "description": "The file path of the README file to format."
                    }
                },
                "required": [
                    "readme_file_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_google_sheet",
            "description": "Executes a Google Sheets-specific formula and returns the computed output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "formula": {
                        "type": "string",
                        "description": "The formula string."
                    }
                },
                "required": [
                    "formula"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_excel_365_sheet",
            "description": "Executes an Office 365-exclusive Excel formula and returns the computed output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "formula": {
                        "type": "string",
                        "description": "The Excel formula to be evaluated as a string."
                    }
                },
                "required": [
                    "formula"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_hidden_input_value",
            "description": "Extracts the value of a hidden input field from an HTML file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_path": {
                        "type": "string",
                        "description": "The path to the HTML file containing the hidden input field."
                    }
                },
                "required": [
                    "html_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_days_in_range",
            "description": "Counts the number of occurrences of a specific day of the week within a given date range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date_str": {
                        "type": "string",
                        "description": "The start date in 'YYYY-MM-DD' format."
                    },
                    "end_date_str": {
                        "type": "string",
                        "description": "The end date in 'YYYY-MM-DD' format."
                    },
                    "target_day_name": {
                        "type": "string",
                        "description": "The name of the day of the week (e.g., 'Monday', 'Wednesday')."
                    }
                },
                "required": [
                    "start_date_str",
                    "end_date_str",
                    "target_day_name"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_answer_from_csv",
            "description": "Downloads and extracts a ZIP file containing a CSV, then retrieves and returns the value in the 'answer' column from the extracted CSV file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "The file path to the ZIP archive."
                    }
                },
                "required": [
                    "zip_file_path"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sort_json_by_age_and_name",
            "description": "Sorts a JSON array of objects by the 'age' field in ascending order and by the 'name' field alphabetically in case of a tie.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_string": {
                        "type": "string",
                        "description": "The input JSON string containing an array of objects."
                    }
                },
                "required": [
                    "json_string"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_txt_to_json_and_hash",
            "description": "Downloads a text file containing key=value pairs, converts them into a single JSON object, computes its hash using an external JSON hashing tool, and returns the resulting hash.",
            "parameters": {
                "type": "object",
                "properties": {
                    "txt_filepath": {
                        "type": "string",
                        "description": "The file path to the text file containing key=value pairs."
                    }
                },
                "required": [
                    "txt_filepath"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_data_values_of_divs",
            "description": "Selects all <div> elements with the class 'foo' from a provided hidden HTML element, extracts their data-value attributes, sums them, and returns the total.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_path": {
                        "type": "string",
                        "description": "The file path to the HTML file."
                    }
                },
                "required": ["html_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_values_for_symbols",
            "description": "Downloads a ZIP archive containing three files with different encodings, parses each file to extract the 'symbol' and 'value' columns, filters rows where the symbol matches a predefined target set, and returns the sum of the associated values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "The file path to the directory containing the data files."
                    },
                    "target_symbols": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of symbols to filter and sum values for."
                    }
                },
                "required": ["zip_file_path", "target_symbols"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_github_repo_and_push_json",
            "description": "Creates a new public GitHub repository, commits and pushes a JSON file named email.json containing a provided email address, and returns the raw GitHub URL of the file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The email address to be stored in the JSON file."
                    }
                },
                "required": ["email_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "replace_iitm_and_compute_sha256",
            "description": "Extracts files from a provided archive, replaces every instance of 'IITM' (in any case variation) with 'IIT Madras' without altering line endings, and finally concatenates the files to return the SHA256 hash computed via 'cat * | sha256sum' in bash.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "The file path to the ZIP archive."
                    }
                },
                "required": ["zip_filepath"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files_and_attributes",
            "description": "Downloads and extracts an archive, lists all files with their modification dates and sizes, filters files that meet a minimum size threshold and a specified modification date, and returns the total size of the matching files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
                    },
                    "min_size": {
                        "type": "integer",
                        "description": "Minimum file size in bytes."
                    },
                    "min_date": {
                        "type": "string",
                        "description": "Minimum modification date in the format 'YYYY-MM-DD HH:MM' (e.g., '1999-02-01 17:40')."
                    }
                },
                "required": [
                    "zip_filepath",
                    "min_size",
                    "min_date"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_rename_files",
            "description": "Downloads and extracts an archive, moves all files from subdirectories into an empty folder, renames each file by replacing every digit with its next value (with '9' wrapping to '0'), and computes the SHA256 hash of the concatenated and sorted file contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
                    }
                },
                "required": [
                    "zip_filepath"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_files",
            "description": "Processes the given ZIP file by extracting it, reading 'a.txt' and 'b.txt', comparing them line by line, and returning the count of differing lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
                    }
                },
                "required": [
                    "zip_filepath"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_sql_query",
            "description": "Generates an SQL query from a natural language description. This function takes a user-provided question or request related to SQL and transforms it into a syntactically correct SQL query. Implement every single instruction (small or big) given in the description",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "A natural language description of the SQL query to generate. This should be a complete request specifying the required SQL operation, table names, columns, and conditions where applicable."
                    }
                },
                "required": [
                    "question"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# GA2 function description
GA2_tools = [
    {
        "type": "function",
        "function": {
            "name": "documentation_markdown",
            "description": "Generates a Markdown document for an imaginary weekly step analysis that includes a level 1 heading, level 2 subheadings, bold text, italic text, inline code (e.g., sample_code), a fenced code block, a bulleted list, a numbered list, a table, a hyperlink, an image, and a blockquote.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compress_and_encode_image",
            "description": "Compresses an image losslessly to ensure it remains under 1,500 bytes while preserving all pixel data, encodes it as Base64, and returns a data URI of the compressed image.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "The file path to the original image."
                    }
                },
                "required": ["input_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_index_html",
            "description": "Publishes a GitHub Pages site showcasing author's work with an email address embedded in the HTML enclosed by <!--email_off--> and <!--/email_off--> tags, and returns the site's public URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Just the email id alone as string to include in the text file."
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_colab_authentication",
            "description": "Runs a Google Colab program that authenticates the user with the required email access and processes their account information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to authenticate and grant access to Google Colab."
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_image_library_colab",
            "description": "Downloads given image, creates a new Google Colab notebook, fixes an error in the provided code, runs the corrected script to calculate the number of pixels above a defined brightness threshold (decimal value between 0 and 1), and returns the pixel count.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "The file path to the image."
                    },
                    "threshold": {
                        "type": "number",
                        "description": "The minimum brightness value (0-1) to consider a pixel as 'bright.'"
                    }
                },
                "required": ["image_path", "threshold"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_to_vercel",
            "description": "Downloads a JSON file containing marks for imaginary students, deploys a Python app on Vercel that exposes an API endpoint accepting multiple 'name' query parameters, and returns a JSON response with the corresponding marks in the order provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_filepath": {
                        "type": "string",
                        "description": "The local path to the JSON file containing student marks."
                    }
                },
                "required": ["json_filepath"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_and_trigger_workflow",
            "description": "Creates a GitHub Action workflow (NO cron/scheduled commits) file in a repository with at least one step whose name includes a specified email address, and returns the URL of the repository where the action is configured.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to include in the GitHub Action step name."
                    }
                },
                "required": [
                    "email"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_and_push_image",
            "description": "Builds and pushes a Docker image to Docker Hub, adds a specific given tag to the image, and returns the Docker image URL in the expected format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "The tag to assign to the container image (e.g., 'daniel.putta')."
                    }
                },
                "required": [
                    "tag"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_fastapi",
            "description": "Downloads a CSV file with 'studentId' and 'class' columns, then creates and runs a FastAPI server with an '/api' endpoint that returns all student records as JSON in the same order as in the CSV, and supports filtering by one or more 'class' query parameters to return only matching records.",
            "parameters": {
                "type": "object",
                "properties": {
                    "csv_filepath": {
                        "type": "string",
                        "description": "The local path to the CSV file containing student data."
                    }
                },
                "required": [
                    "csv_filepath"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "setup_llamafile_with_ngrok",
            "description": "Downloads the Llamafile, runs the Llama-3.2-1B-Instruct.Q6_K.llamafile model using it, creates an ngrok tunnel to the server, and returns the public ngrok URL.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# GA3 function description
GA3_tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_sentiment_test_code",
            "description": "Generates a Python program that uses httpx to send a POST request to OpenAI's API for sentiment analysis testing. The program inserts the provided meaningless text exactly as given. The meaningless text is a raw string containing arbitrary characters, and it is not expected to form a coherent sentence.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sample_meaningless_text": {
                        "type": "string",
                        "description": "A meaningless string (e.g., random characters, numbers, or symbols) that should be inserted verbatim into the generated code. This text will be used as-is without any modifications."
                    }
                },
                "required": ["sample_meaningless_text"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_and_count_tokens",
            "description": "Computes the number of tokens used in a given user message for tokenization analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The user message to be tokenized, typically provided in a test case."
                    }
                },
                "required": [
                    "text"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_openai_address_request",
            "description": "Generates the JSON body for an OpenAI chat completion request to generate U.S. address data. The function expects an argument 'fields' that is an array of objects. Each object should have a 'field' key (the required field name) and a 'type' key (the expected datatype, e.g., 'string' or 'number'). The LLM should dynamically extract and output these field names and types based on the query.",
            "parameters": {
            "type": "object",
            "properties": {
                "fields": {
                "type": "array",
                "description": "An array of objects, each specifying a required field with its name and type.",
                "items": {
                    "type": "object",
                    "properties": {
                    "field": {
                        "type": "string",
                        "description": "The name of the required field."
                    },
                    "type": {
                        "type": "string",
                        "description": "The expected datatype (e.g., 'string' or 'number')."
                    }
                    },
                    "required": ["field", "type"],
                    "additionalProperties": False
                }
                }
            },
            "required": ["fields"],
            "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "base64_encoding",
            "description": "Encodes an invoice image in base64 and generates a JSON request body for OpenAI's API to extract text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "The file path to the invoice image containing text that needs extraction."
                    }
                },
                "required": ["image_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_embedding_request",
            "description": "Generates a JSON payload for requesting text embeddings from OpenAI's API. This is used in fraud detection to analyze transaction verification messages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of personalized transaction verification messages, each containing a transaction code and an email address. These messages are analyzed for fraud detection."
                    }
                },
                "required": ["messages"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "return_most_similar_function",
            "description": "Returns a multiline string containing Python code that implements a function to compute cosine similarity between embedding vectors and identify the pair of phrases with the highest similarity.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "docs_similarity_api_endpoint",
            "description": "Creates a FastAPI-based semantic search service built for InfoCore Solutions and return its the API endpoint URL. This service is implemented as a POST endpoint at '/similarity' and accepts a JSON payload containing 'docs' (an array of document texts from an internal knowledge base) and 'query' (a search query string). The service computes text embeddings using the 'text-embedding-3-small' model for both documents and query, calculates cosine similarity scores, and returns the top three matching documents ranked by similarity. The FastAPI application also enables CORS to allow all origins and headers, and supports OPTIONS and POST methods.",
            "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "employee_queries_api_endpoint",
            "description": "Create a FastAPI service that maps employee queries to specific function calls for TechNova Corp and return the API endpoint URL. The service exposes a GET endpoint at '/execute' which accepts a query parameter 'q' containing pre-templatized queries (such as checking ticket status, scheduling meetings, retrieving expense balances, calculating performance bonuses, and reporting office issues). The backend analyzes the query, extracts the required parameters, and returns a JSON response with the function name and a JSON-encoded string of arguments. CORS is enabled to allow GET requests from any origin.",
            "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_prompt",
            "description": "Generates a prompt that attempts to make the Language Model say 'Yes'.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# GA4 function description
GA4_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ducks_sum",
            "description": "Counts the total number of ducks (players out for 0 runs) on a specific page of ESPN Cricinfo's ODI batting statistics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page_number": {
                        "type": "integer",
                        "description": "The page number of the ESPN Cricinfo ODI batting stats to fetch and analyze."
                    }
                },
                "required": ["page_number"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_imdb_movies",
            "description": "Fetches a list of movies from IMDb that fall within a specified IMDb rating range using the IMDb's advanced web search at https://www.imdb.com/search/title/ to access movie data. The function retrieves details such as movie ID, title, release year, and rating from the first 25 results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_rating": {
                        "type": "number",
                        "description": "The minimum IMDb rating to filter movies."
                    },
                    "max_rating": {
                        "type": "number",
                        "description": "The maximum IMDb rating to filter movies."
                    }
                },
                "required": ["min_rating", "max_rating"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "country_outline_api_endpoint",
            "description": "Creates a Fastapi service to retrieving a structured Markdown outline of a Wikipedia page for a specified country and returns the API endpoint URL. This API extracts headings (H1 to H6) from the page, maintains their hierarchical order, and formats them as an outline. The endpoint allows querying by country name and supports CORS for seamless integration into educational tools.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast_description",
            "description": "Fetches the weather forecast for a given city using the BBC Weather API. The function retrieves the location ID for the specified city, then extracts forecast details such as the date and a detailed weather description, returning a structured JSON response.",
            "parameters": {
                "type": "object",
                "properties": {
                    "required_city": {
                        "type": "string",
                        "description": "The name of the city for which the weather forecast is requested."
                    }
                },
                "required": ["required_city"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_maximum_latitude",
            "description": "Retrieves the maximum latitude of the bounding box for a given city in a specified country using the Nominatim API. The function sends a request to fetch geospatial data and extracts the highest latitude value from the bounding box coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "The name of the country where the city is located."
                    },
                    "city": {
                        "type": "string",
                        "description": "The name of the city for which the maximum latitude is required."
                    }
                },
                "required": ["country", "city"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_most_recent_link",
            "description": "Retrieves the most recent Hacker News post that contains a specified keyword and has at least a given number of points. It queries the HNRSS API, filters the results, and returns the URL of the most relevant post.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "The topic or keyword to search for in Hacker News posts."
                    },
                    "min_points": {
                        "type": "integer",
                        "description": "The minimum number of points a post must have to be considered relevant."
                    }
                },
                "required": ["keyword", "min_points"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_most_recent_valid_user",
            "description": "Finds the most recently created GitHub user account in a specified city that has at least a given number of followers and was created before a specified date. The function queries the GitHub API, filters users based on the given criteria, and returns the creation date of the newest qualifying user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city to search for GitHub users (e.g., 'Bangalore')."
                    },
                    "min_followers": {
                        "type": "integer",
                        "description": "The minimum number of followers a user must have to be considered."
                    },
                    "max_date_time": {
                        "type": "string",
                        "description": "The latest possible account creation date in ISO 8601 UTC format (e.g., '2024-01-01T00:00:00Z')."
                    }
                },
                "required": ["location", "min_followers", "max_date_time"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_github_action_workflow",
            "description": "Generates a GitHub Actions workflow that uses 'cron' to schedule a daily commit to the repository, appending the current date to a file. A step in the workflow is named using the provided email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The email address to be included in the name of one of the workflow steps."
                    }
                },
                "required": ["email_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_total_marks",
            "description": "Calculates the total marks in a specified subject for students who meet or exceed a given score in another subject, within a specified group range. The data is extracted from a PDF file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the PDF file containing the student marks table."
                    },
                    "group_range_str": {
                        "type": "string",
                        "description": "Range of groups to filter, in the format 'start-end' (e.g., '16-45')."
                    },
                    "filter_marks": {
                        "type": "integer",
                        "description": "Minimum score threshold for the filter subject."
                    },
                    "main_subject": {
                        "type": "string",
                        "description": "The subject for which to calculate the total marks."
                    },
                    "filter_subject": {
                        "type": "string",
                        "description": "The subject used to apply the score filter."
                    }
                },
                "required": ["filepath", "group_range_str", "filter_marks", "main_subject", "filter_subject"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pdf_to_markdown",
            "description": "Converts a PDF file to Markdown format, ensuring proper formatting using headings, lists, tables, and code blocks. The final Markdown output is formatted using Prettier 3.4.2 for consistency.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pdf_filepath": {
                        "type": "string",
                        "description": "The file path to the PDF document that needs to be converted into Markdown."
                    }
                },
                "required": ["pdf_filepath"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# GA5 function description
GA5_tools = [
    {
        "type": "function",
        "function": {
            "name": "clean_and_calculate_margin",
            "description": "Cleans an Excel file of sales transaction records and calculates the total margin for filtered transactions. The function standardizes country names, dates, product names, and financial values before filtering transactions based on product, country, and date. The margin is computed as (Total Sales - Total Cost).",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The file path to the Excel file containing sales transaction records."
                    },
                    "target_product": {
                        "type": "string",
                        "description": "The product name used to filter transactions (e.g., 'Epsilon')."
                    },
                    "target_country": {
                        "type": "string",
                        "description": "The standardized country code used to filter transactions (e.g., 'AE' for United Arab Emirates)."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date (inclusive) for filtering transactions. The date must be in a ISO 8601 format (e.g., 2022-12-01T15:09:28+05:30)."
                    }
                },
                "required": ["file_path", "target_product", "target_country", "end_date"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_unique_students",
            "description": "Reads a text file, extracts student IDs (numbers after 'Marks'), removes duplicates, and returns the count of unique student IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file containing student records."
                    }
                },
                "required": ["file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_successful_get_requests",
            "description": "Counts the number of successful GET requests for a specific language section within a given time frame on a specified day from an Apache log file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_file_path": {
                        "type": "string",
                        "description": "Path to the Apache log file."
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time in 'HH:MM' format (24-hour clock) representing the beginning of the time window."
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in 'HH:MM' format (24-hour clock) representing the end of the time window."
                    },
                    "language": {
                        "type": "string",
                        "description": "Language section to filter the requests (e.g., 'telugu' for URLs under '/telugu/')."
                    },
                    "day": {
                        "type": "string",
                        "description": "Day of the week to filter the requests (e.g., 'Sunday')."
                    }
                },
                "required": ["log_file_path", "start_time", "end_time", "language", "day"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_apache_log",
            "description": "Analyzes an Apache log file to determine the total number of bytes downloaded by the top IP address for a specific page section on a given date, considering only successful requests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_file_path": {
                        "type": "string",
                        "description": "The file path to the GZipped Apache log file."
                    },
                    "page_section": {
                        "type": "string",
                        "description": "The URL path prefix to filter requests (e.g., '/telugump3/')."
                    },
                    "date": {
                        "type": "string",
                        "description": "The date to filter requests in 'YYYY-MM-DD' format (e.g., '2024-05-13')."
                    }
                },
                "required": ["log_file_path", "page_section", "date"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_sales_data",
            "description": "Processes a JSON dataset of sales entries to determine the total number of units sold for a given product in a specified city, using phonetic clustering for city name variations and filtering transactions based on a minimum units sold threshold.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_file_path": {
                        "type": "string",
                        "description": "The file path to the JSON file containing sales entries."
                    },
                    "city": {
                        "type": "string",
                        "description": "The target city to filter and aggregate sales (e.g., 'London')."
                    },
                    "product": {
                        "type": "string",
                        "description": "The product to filter on (e.g., 'Pizza')."
                    },
                    "min_sales": {
                        "type": "integer",
                        "description": "The minimum number of units sold in a transaction for it to be considered."
                    }
                },
                "required": ["json_file_path", "city", "product", "min_sales"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_total_sales_jsonl",
            "description": "Calculates the total sales from a JSONL file containing sales data. Each line in the file is a JSON object with a 'sales' field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "jsonl_file_path": {
                        "type": "string",
                        "description": "The file path to the JSONL file containing sales data."
                    }
                },
                "required": ["jsonl_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_key_occurrences",
            "description": "Counts the number of times a specific key appears in a nested JSON structure.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_file_path": {
                        "type": "string",
                        "description": "The file path to the JSON file."
                    },
                    "target_key": {
                        "type": "string",
                        "description": "The key to count within the JSON structure."
                    }
                },
                "required": ["json_file_path", "target_key"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_duckdb_query",
            "description": "Generates a DuckDB SQL query to extract post IDs for high-impact posts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_timestamp": {
                        "type": "string",
                        "description": "The minimum timestamp to filter posts in ISO 8601 UTC format (e.g., '2025-01-05T18:02:26.045Z')."
                    },
                    "min_useful_stars": {
                        "type": "integer",
                        "description": "The threshold for the minimum number of useful stars a comment must have."
                    }
                },
                "required": ["min_timestamp", "min_useful_stars"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_and_transcribe",
            "description": "Generates a transcript for a specific segment of a YouTube video.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "number",
                        "description": "The starting time (in seconds) of the segment to be transcribed (e.g., 108.8)."
                    },
                    "stop_time": {
                        "type": "number",
                        "description": "The ending time (in seconds) of the segment to be transcribed (e.g., 282.6)."
                    }
                },
                "required": ["start_time", "stop_time"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reconstruct_image",
            "description": "Reconstructs an image from its scrambled pieces using a specified mapping of piece positions. The function takes a scrambled image file and a mapping list that details how each scrambled piece should be repositioned to restore the original image. The output is a base64-encoded WEBP image, representing the reconstructed version.",
            "parameters": {
                "type": "object",
                "properties": {
                    "scrambled_image_path": {
                        "type": "string",
                        "description": "The file path to the scrambled image that needs to be reconstructed."
                    },
                    "mapping": {
                        "type": "array",
                        "description": "A list of mappings defining how scrambled pieces should be repositioned. Each mapping is a tuple containing four integers: (original_row, original_col, scrambled_row, scrambled_col).",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "integer"
                            },
                            "description": "A tuple containing four integers (original_row, original_col, scrambled_row, scrambled_col), indicating where each scrambled piece should be placed in the reconstructed image."
                        }
                    }
                },
                "required": ["scrambled_image_path", "mapping"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]