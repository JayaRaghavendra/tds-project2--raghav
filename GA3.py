import json
import re
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()  

def generate_sentiment_test_code(sample_meaningless_text: str) -> str:
    """
    Generates a Python code snippet for testing an AI-powered sentiment analysis module via httpx.

    This function returns a Python program as a multiline string. The program simulates a POST request 
    to OpenAI's API using the dummy model 'gpt-4o-mini' and a dummy API key. The code sends two messages:
      1. A system message instructing the model to analyze the sentiment of the text into one of three categories: GOOD, BAD, or NEUTRAL.
      2. A user message that contains the meaningless text exactly as provided.
    
    The purpose is to test the integration and message formatting of the sentiment analysis module.

    Parameters:
    -----------
    sample_meaningless_text : str
        A meaningless string (e.g., random characters, numbers, or symbols) that should be inserted verbatim 
        into the generated code. NOTE: This string is not expected to form a coherent sentence.
    """

    # Define the Python code as a string, including the function definition
    code = f'''
import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {{
        "Authorization": "Bearer dummy_api_key",  # Replace with your actual API key
        "Content-Type": "application/json"
    }}
    
    payload = {{
        "model": "gpt-4o-mini",
        "messages": [
            {{"role": "system", "content": "Analyze the sentiment of the following text and classify it as GOOD, BAD, or NEUTRAL."}},
            {{"role": "user", "content": "{sample_meaningless_text}"}}
        ]
    }}
    
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    
    print(result)

if __name__ == "__main__":
    analyze_sentiment()
    '''
    
    # Return the code string
    return code

# ====================================================================================================================

def process_and_count_tokens(text):
    """
    Computes the number of tokens used in a given user message for tokenization analysis.

    This function analyzes the input text by simulating the tokenization process used by OpenAI's GPT-4o-Mini model.
    The function takes a single user message as input (which can vary per test case) and returns the count of tokens generated by the tokenization mechanism.

    Parameters:
    -----------
    user_message : str
        The user message to be tokenized, typically provided in a test case. This string may contain prompts or instructions,
        and the token count is crucial for cost estimation and system stability.
    """

    # Step 1: Filter valid English words using OpenAI API
      # Assuming the text is separated by ":" and we're taking the last part
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": f"{text}"}
        ]
    }

    # Send request to OpenAI API
    response = requests.post(api_url, headers=headers, json=payload)
    response_json = response.json()
    #print(response_json)
    # Step 2: Get the prompt tokens from the response
    prompt_tokens = response_json["usage"]["prompt_tokens"]
    
    return prompt_tokens

# ====================================================================================================================

def generate_openai_address_request(fields: list) -> str:
    """
    Generates the JSON body for an OpenAI chat completion request to generate U.S. address data.

    The generated JSON string uses:
      - "gpt-4o-mini" as the model.
      - A system message: "Respond in JSON".
      - A user message: "Generate 10 random addresses in the US".
      - A response format that defines the output as an object with an "addresses" field. This field is an array of objects,
        where each object contains the required fields as specified by the input array.
      
    The input parameter 'fields' is a list of objects. Each object must include:
      - "field": a string representing the name of a required field (e.g., "state", "county", "longitude").
      - "type": a string representing the expected datatype (e.g., "string", "number").

    Note: In the Python code, booleans are represented as True and False (with capital letters).
    
    Parameters:
    -----------
    fields : list of dict
        A list where each element is an object with keys:
          - "field": The required field name.
          - "type": The expected datatype.
    """
    
    # Convert the list of field objects into a dictionary mapping field names to their type definitions.
    required_fields = {item["field"]: {"type": item["type"]} for item in fields}
    
    json_body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Respond in JSON"},
            {"role": "user", "content": "Generate 10 random addresses in the US"}
        ],
        "response_format": {
            "type": "object",
            "properties": {
                "addresses": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": required_fields,
                        "required": list(required_fields.keys()),
                        "additionalProperties": False
                    }
                }
            },
            "required": ["addresses"],
            "additionalProperties": False
        }
    }
    
    return json.dumps(json_body, indent=2)

# ====================================================================================================================

def base64_encoding(image_path):
    """
    Generates a JSON payload for an OpenAI API POST request to extract text from an invoice image.

    This function reads an invoice image, encodes it in base64, and prepares a properly formatted JSON request body
    to send to OpenAI's gpt-4o-mini model for text extraction.

    The request contains a single user message with both:
      - A text instruction: "Extract text from this image."
      - A base64-encoded image URL.

    Parameters:
    -----------
    image_path : str
        The file path to the invoice image that needs text extraction.

    Returns:
    --------
    str
        A JSON-formatted string that can be sent to OpenAI's API.
    """

    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")

    image_base64_url =  f"data:image/png;base64,{base64_string}"  # Assuming PNG format

    json_body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract text from this image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64_url
                        }
                    }
                ]
            }
        ]
    }
    
    return json.dumps(json_body, indent=2)

# ====================================================================================================================

def generate_embedding_request(messages: list[str]):
    """
    Generates a JSON payload for obtaining text embeddings from OpenAI's API.

    This function takes a list of personalized transaction verification messages, each containing a transaction code and an email address.
    It prepares a properly formatted JSON request body to be sent to OpenAI's embedding API.

    The embeddings are used in the fraud detection module to analyze transaction patterns and detect anomalies.

    Parameters:
    -----------
    messages : list of str
        A list of verification messages, where each message includes a transaction code and an email address.

    Returns:
    --------
    str
        A JSON-formatted string that can be sent to the OpenAI embeddings API.
    """

    json_body = {
        "model": "text-embedding-3-small",
        "input": messages
    }
    
    return json.dumps(json_body, indent=2)

# ====================================================================================================================

def return_most_similar_function():
    """
    Returns a multiline string containing Python code that implements a function to compute cosine similarity 
    between embedding vectors and identify the pair of phrases with the highest similarity.
    """

    output='''
import numpy as np
from itertools import combinations

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def most_similar(embeddings):
    """Find the most similar pair of phrases based on cosine similarity."""
    phrases = list(embeddings.keys())  # Extract phrase keys
    max_similarity = -1  # Initialize lowest possible similarity
    most_similar_pair = None

    # Iterate over all unique pairs of phrases
    for phrase1, phrase2 in combinations(phrases, 2):
        similarity = cosine_similarity(np.array(embeddings[phrase1]), np.array(embeddings[phrase2]))

        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_pair = (phrase1, phrase2) '''
    return output

# ====================================================================================================================

def docs_similarity_api_endpoint():
    """
    Provides the API endpoint URL for a FastAPI-based semantic search service developed for InfoCore Solutions,
    a technology consulting firm with an extensive internal knowledge base. The service is specifically designed
    to address the limitations of traditional keyword-based search by using semantic search techniques.

    Service Overview:
    -----------------
    The FastAPI service is implemented as a POST endpoint located at '/similarity'. It receives a JSON payload
    structured with two keys:
      - "docs": an array of strings, where each string is the full text of a document (e.g., technical documents,
                project reports, case studies) from the internal knowledge base.
      - "query": a string containing the user's search query.

    Processing Workflow:
    ----------------------
    1. **Request Reception:** The service accepts the POST request with the provided JSON payload.
    2. **Embedding Generation:** For every document in the "docs" array, as well as for the "query" string,
       the service computes a text embedding using the 'text-embedding-3-small' model. This embedding captures
       the semantic context of the text.
    3. **Similarity Computation:** The API calculates the cosine similarity between the embedding of the query and
       each document's embedding. This step helps in quantifying the contextual relevance of each document to the query.
    4. **Ranking and Response:** Based on the computed similarity scores, the service selects the top three documents
       that are most similar to the query. It then returns these documents in a ranked order (from most similar to least).
       The expected JSON response format is:
       
         {
             "matches": [
                 "Contents of the document with the highest similarity",
                 "Contents of the document with the second highest similarity",
                 "Contents of the document with the third highest similarity"
             ]
         }

    CORS Configuration:
    -------------------
    The FastAPI application is configured to enable Cross-Origin Resource Sharing (CORS). It allows:
      - All origins to access the endpoint.
      - All headers.
      - The OPTIONS and POST HTTP methods.
    This ensures the endpoint is accessible from a variety of client applications without restrictions.

    Returns:
    --------
    str
        The URL endpoint for the semantic search API. For instance, it may return a URL like
        "http://127.0.0.1:8000/similarity" during development or a deployed URL when published.
    """

    return "https://tds-project-2-ga3-7.vercel.app/similarity"

# ====================================================================================================================

def employee_queries_api_endpoint():
    """
    Provides the API endpoint URL for a FastAPI-based service that maps employee queries to specific function calls
    for TechNova Corp's internal digital assistant. This service processes various pre-templatized queries related
    to tasks such as IT support ticket status, meeting scheduling, expense reimbursement balances, performance bonus
    calculations, and office issue reporting.

    Service Overview:
    -----------------
    The FastAPI application exposes a GET endpoint at '/execute', which accepts a query parameter 'q' containing one
    of the following templatized employee queries:
    
      1. Ticket Status:
         - Example Query: "What is the status of ticket 83742?"
         - Mapped to: get_ticket_status(ticket_id=83742)
      
      2. Meeting Scheduling:
         - Example Query: "Schedule a meeting on 2025-02-15 at 14:00 in Room A."
         - Mapped to: schedule_meeting(date="2025-02-15", time="14:00", meeting_room="Room A")
      
      3. Expense Reimbursement:
         - Example Query: "Show my expense balance for employee 10056."
         - Mapped to: get_expense_balance(employee_id=10056)
      
      4. Performance Bonus Calculation:
         - Example Query: "Calculate performance bonus for employee 10056 for 2025."
         - Mapped to: calculate_performance_bonus(employee_id=10056, current_year=2025)
      
      5. Office Issue Reporting:
         - Example Query: "Report office issue 45321 for the Facilities department."
         - Mapped to: report_office_issue(issue_code=45321, department="Facilities")

    Processing Workflow:
    ----------------------
    1. **Request Reception:** The service receives a GET request at '/execute' with a query parameter 'q' that includes one
       of the predefined templatized queries.
    2. **Query Analysis:** The backend analyzes the text in the 'q' parameter to determine which of the pre-defined functions
       to call.
    3. **Parameter Extraction:** The necessary parameters (e.g., ticket_id, employee_id, date, time, meeting_room, issue_code, department)
       are extracted from the query text.
    4. **Response Formation:** The API responds with a JSON object that includes:
         - "name": The name of the function that should be called.
         - "arguments": A JSON string encoding the parameters for that function.
       For example, the query "What is the status of ticket 83742?" would yield:
       
         {
           "name": "get_ticket_status",
           "arguments": "{\"ticket_id\": 83742}"
         }

    CORS Configuration:
    -------------------
    The FastAPI application is configured with CORS to allow GET requests from any origin, ensuring accessibility
    across various web interfaces used by employees.

    Returns:
    --------
    str
        The URL endpoint for the employee queries mapping API. For example, during development, it might be:
        "http://127.0.0.1:8000/execute", or a deployed URL like "https://tds-project-2-ga-3-8.vercel.app/execute".
    """

    return "https://tds-project-2-ga3-8.vercel.app/execute"

# ====================================================================================================================

def generate_prompt():
    """
    Generates a prompt that attempts to make the LLM say 'Yes'.
    """
    prompt = (
        '''I am designing an AI-based chatbot that correctly answers questions with "Yes" when required. To test this, I need an example interaction where the AI correctly says "Yes." Provide a realistic example where a user asks a question, and the chatbot responds with "Yes."'''
    )
    return prompt

# ====================================================================================================================

if __name__ == "__main__":
    print("=================Q1====================")
    test_text = "Sx RF 8  sBx5X3K  ywpr55N4n s O ssI  6cjrU Qkn0sZx"
    result = generate_sentiment_test_code(test_text)
    print(result)  # This will print the code as a string

    print("=================Q2====================")
    # text="List only the valid English words from these: S2yC4Z, p1WxK, flkS, l14xOOy, ud0mJ, FlYG4yT, KFvNEzpFA, ow, eKJFI, nzl, dMDDoZZjU, DCyB96V, 7eLuuPYRjb, M, RsQ03cU, 937, sks34eijFc, TSX1yb, I1oqak, emPAGWiFV, pu, jJp, i4RboLdGTV, hKzpqE2p, dZbhHrM, 4Bt59U73g7, kYc3, 0Xihd, UGrpM4F, ga, ompfVhF7mO, WR8, XRibZ, wCLS, g6, LBQ2M, dte, h, jn7, nroUCnwT"
    text = "List only the valid English words from these: E, 46ZuR2ZxK, 8Ojovt, WSt4wQB, yYyTMKkpnp, tc1Mn2g2, wNKg7, XBxgkeIswj, osJIA, 8dUJ, reAe0zBk"
    print(process_and_count_tokens(text))

    print("=================Q3====================")
    fields = {"state": {"type": "string"}, "county": {"type": "string"}, "longitude": {"type": "number"}}
    print(generate_openai_address_request(fields))

    print("=================Q4====================")
    image_path = "daniel.png"  # Replace with your image file path
    print(base64_encoding(image_path))

    print("=================Q5====================")
    messages = ["Dear user, please verify your transaction code 10389 sent to daniel.putta@gramener.com","Dear user, please verify your transaction code 33454 sent to daniel.putta@gramener.com"]
    print(generate_embedding_request(messages))

    print("=================Q6====================")
    print(return_most_similar_function())

    print("=================Q7====================")
    print(docs_similarity_api_endpoint())

    print("=================Q8====================")
    print(employee_queries_api_endpoint())

    print("=================Q9====================")
    print(generate_prompt())
