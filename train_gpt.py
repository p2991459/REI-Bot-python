import json
import openai
import os
from gpt3 import GPT, Example
openai.api_key = os.getenv("OPENAI_API_KEY")
gpt = GPT(engine="text-davinci-003",
          temperature=0.5,
          max_tokens=1048,
          )

#TODO: Refect the code to use data from database instead of using jsonl file.
with open('responses.jsonl', 'r') as f:
    # Iterate through each line in the file
    linen  = 1
    for line in f:
        data = json.loads(line)
        prompt = data['prompt']
        # print("Line number:" ,linen)
        completion = data['completion']
        gpt.add_example(Example(prompt, completion))
        linen+= 1


