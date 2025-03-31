from GA1 import *
from GA2 import *

GA1_tools = [
    {
        "type": "function",
        "function": {
            "name": "run_code_status",
            "description": "Runs a shell command to check the status of the code repository.",
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
            "description": "Runs an HTTP request to httpbin.org with the given email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_address": {
                        "type": "string",
                        "description": "The email address to include in the request."
                    }
                },
                "required": ["email_address"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_prettier",
            "description": "Formats the specified README file using Prettier and calculates its SHA-256 checksum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "readme_file_path": {
                        "type": "string",
                        "description": "The file path of the README file to format."
                    }
                },
                "required": ["readme_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_google_sheet",
            "description": "Puts a formula in a google sheet at A1 cell, computes in B1, and returns the result from B1.",
            "parameters": {
                "type": "object",
                "properties": {
                    "formula": {
                        "type": "string",
                        "description": "The formula string."
                    }
                },
                "required": ["formula"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_excel_365_sheet",
            "description": "Evaluates a given Excel formula in Excel 365 and returns its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "formula": {
                        "type": "string",
                        "description": "The Excel formula to be evaluated as a string."
                    }
                },
                "required": ["formula"],
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
                "required": ["html_path"],
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
                "required": ["start_date_str", "end_date_str", "target_day_name"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_answer_from_csv",
            "description": "Extracts and returns the value from the 'answer' column in the extract.csv file inside a given ZIP archive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "The file path to the ZIP archive."
                    }
                },
                "required": ["zip_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sort_json_by_age_and_name",
            "description": "Sorts a JSON array of objects by the 'age' field in ascending order. In case of a tie, sorts by the 'name' field alphabetically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_string": {
                        "type": "string",
                        "description": "The input JSON string containing an array of objects."
                    }
                },
                "required": ["json_string"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_txt_to_json_and_hash",
            "description": "Reads a text file containing key=value pairs, converts it into a single JSON object, and computes its hash using the online tool at tools-in-data-science.pages.dev/jsonhash.",
            "parameters": {
                "type": "object",
                "properties": {
                    "txt_filepath": {
                        "type": "string",
                        "description": "The file path to the text file containing key=value pairs."
                    }
                },
                "required": ["txt_filepath"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_data_values_of_divs",
            "description": "Parses an HTML file, finds all <div> elements with the class 'foo' inside a hidden element, and sums their 'data-value' attributes.",
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
            "description": "Reads and processes three differently encoded files, summing values for specific symbols across all files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "The file path to the directory containing the three data files."
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
            "description": "Automates the process of creating a GitHub repository, committing a JSON file, and pushing it to GitHub.",
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
            "description": "Extracts a ZIP archive, replaces all occurrences of 'IITM' (case-insensitive) with 'IIT Madras' in all files, and computes the SHA-256 checksum of the concatenated file contents.",
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
            "description": "Processes the given ZIP file by extracting it into a folder named '<zipfilename>_unzipped' (preserving timestamps), using 'ls -l --time-style=long-iso' to list files with their modification date and size, filtering files that are at least min_size bytes and modified on or after min_date, and summing their sizes using an awk command.",
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
                "required": ["zip_filepath", "min_size", "min_date"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_rename_files",
            "description": "Processes the given ZIP file by extracting it into a folder named '<zipfilename>_unzipped' while preserving file timestamps, moving all files (recursively) from the extracted folder into a new empty folder ('flat'), renaming all files in the flat folder by replacing each digit with the next digit (with 9 wrapping to 0; e.g., a1b9c.txt becomes a2b0c.txt), running the shell command 'grep . * | LC_ALL=C sort | sha256sum' in that folder, and returning the output of the shell command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
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
            "name": "compare_files",
            "description": "Processes the given ZIP file by deleting the destination folder ('<zipfilename>_unzipped') if it exists, creating a new destination folder, extracting the ZIP file into that folder while preserving file timestamps, reading 'a.txt' and 'b.txt' from the folder, comparing the two files line by line to count how many lines differ, and returning the count of differing lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
                    }
                },
                "required": ["zip_filepath"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

from GA2 import *

# similar to GA1_tools for functions in GA1.py, create GA2_tools for functions in GA2.py
GA2_tools = [
    {
        "type": "function",
        "function": {
            "name": "documentation_markdown",
            "description": "Generates a Markdown-formatted analysis of daily step counts over a week, comparing trends over time and with friends.",
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
            "description": "Compresses an image losslessly into WebP format and returns a Base64 encoded data URI.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "The file path to the source image."
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
        "function":{
            "name": "update_index_html",
            "description": "Update the index.html file in a GitHub repository with the new content",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to include in the HTML comment."
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
            "description": "Authenticates user in Colab, retrieves user info, and returns the hashed value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_info": {
                        "type": "string",
                        "description": "The user information to be hashed."
                    }
                },
                "required": ["user_info"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_image_library_colab",
            
        }
    }
]