import openai
import jsonlines
import os
# Set up OpenAI API key

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define prompts
prompts = [
    "User: I'm feeling really anxious about giving a presentation. What can I do?\nBot:",
    "User: I'm feeling really angry and frustrated with my partner. How can I handle this?\nBot:",
    "User: I'm feeling overwhelmed with work and personal responsibilities. How can I manage my stress?\nBot:",
    "User: I'm feeling sad and hopeless. How can I start feeling better?\nBot:",
    "User: I'm feeling guilty about something I did in the past. How can I move forward?\nBot:",
    "User: I'm feeling anxious about meeting new people. How can I overcome this fear?\nBot:",
    "User: I'm feeling insecure about my abilities. How can I build my confidence?\nBot:",
    "User: I'm feeling resentful towards a friend who let me down. How can I address this issue?\nBot:",
    "User: I'm feeling overwhelmed with negative thoughts. How can I challenge and change them?\nBot:",
    "User: I'm feeling jealous of someone else's success. How can I overcome this feeling?\nBot:",
    "User: I'm feeling uncertain about a major decision I have to make. How can I approach it more rationally?\nBot:"
]

# Define model engine
model_engine = "text-davinci-002"

# Generate responses and save them to a file in JSONL format
with jsonlines.open('responses.jsonl', mode='w') as writer:
    for prompt in prompts:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        writer.write({'prompt': prompt, 'response': response.choices[0].text.strip()})
