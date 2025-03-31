from GA1 import *
from GA2 import *
from GA3 import *
from GA4 import *
from GA5 import *
from func_desc import *
from llm_utils import *
import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def agent(input_str, file_path):
    logging.info(f"Question: {input_str}")
    input_modified_str = input_str + "\n" + f"File is {file_path}" if file_path else input_str
    response = query_gpt(input_modified_str, GA1_tools+GA2_tools+GA3_tools+GA4_tools+GA5_tools)
    logging.info(f"Response: {response}")
    logging.info(f"Tools: {response.get("tool_calls",[])}")
    function_call_details = [tool_call["function"] for tool_call in response["tool_calls"]][0]
    logging.info(f"Function details loaded: {function_call_details}")

    # Call the function with the filepath
    func = globals()[function_call_details['name']]
    arguments = json.loads(function_call_details['arguments'])
    logging.info(f"Executing function: {function_call_details['name']} with arguments: {arguments}")
    func_output = func(**arguments)
    return func_output

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],         # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],         # Allows all headers
)

@app.post("/api/")
async def process_request(
    question: str = Form(...),
    file: UploadFile = File(None)
):
    # Read the question from the form.
    input_question = question

    # Read the file if provided.
    file_content = None
    file_path = None
    if file:
        file_content = await file.read()
        file_path = file.filename
        with open(file_path, "wb") as f:
            f.write(file_content)

    # Call the agent function
    output = agent(input_question, file_path)
    output = str(output) if not isinstance(output, str) else output
    response = {"answer": output.strip()}

    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)