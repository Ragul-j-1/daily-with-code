import json
from app.prompts import CANDIDATE_EVALUATION
import requests

def candidate_evaluation(candidate_details :str , jd:str)-> str:
    prompt=CANDIDATE_EVALUATION.format(resume_json=candidate_details,job_description_json=jd)
    try:
        response=requests.post(
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