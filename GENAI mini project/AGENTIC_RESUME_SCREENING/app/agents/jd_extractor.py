import requests
import json
from app.prompts import EXTRACT_JD_DETAILS

def extract_jd_data(text:str):
    prompt=EXTRACT_JD_DETAILS.format(jd_text=text)
    response=requests.post(
      "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1:1.5b",
            "prompt": prompt
        },
        stream=True
    )
    final_output=""
    for line in response.iter_lines():
        if line:
            data=json.loads(line.decode("utf-8"))
            token=data.get("response","")
            final_output+=token
    print(final_output)
    return final_output
    