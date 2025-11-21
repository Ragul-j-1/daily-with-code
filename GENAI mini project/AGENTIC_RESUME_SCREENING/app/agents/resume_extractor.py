import requests
import json
from app.prompts import EXTRACT_CANDIDATE_DETAILS

def extract_resume_data(resume_text: str):
    prompt = EXTRACT_CANDIDATE_DETAILS.format(resume_text=resume_text)
    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": prompt
            },
            stream=True
        )

        final_output = ""

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                final_output += token

        print(final_output)
        return final_output
    except Exception as e:
        return{"error":str(e)}
