from train_gpt import gpt
import time
from flask import Flask, request, jsonify, render_template
import json
import os
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    #TODO: Dump the previous conversation to responses.jsonl and delete the json file
    #DONE: Delete last conversation json file to prevent overriding
    filename = 'last_conversation.json'
    if os.path.exists(filename):  # Check if file exists in current directory
        os.remove(filename)  # Delete the file
        print(f"{filename} has been deleted successfully!")
    else:
        print(f"{filename} does not exist in the current directory.")
    return render_template('index.html')

@app.route('/gpt_response', methods=['GET', 'POST'])
def gpt_response():
    if request.method == 'POST':
        request_data = request.data.decode('utf-8').split('=')
        result_dict = {request_data[0]: request_data[1]}
        user_input = result_dict["text"]
        #TODO: Take Previous conversations through conversation_id and add them to the user input to get response based on history chat
        try:
            conv_data = json.loads(open("last_conversation.json").read())
            print(conv_data)
            first_user_message = conv_data[1]
            prompt = f"User:{first_user_message['text']}\nBot: "

            if len(conv_data) >= 2:
                print(conv_data)
                for conv in conv_data[2:]:
                    if conv['from'] == 'user':
                        prompt += f"\nUser: {conv['text']}\nBot: "
                    else:
                        prompt += f"{conv['text']}"
            print(prompt)
            prompt = prompt+f"\nUser: {user_input}\nBot: "
            print(prompt,"prompt after update the latest user message")
            p = gpt.submit_request(prompt)
            return p['choices'][0]['text']
        except FileNotFoundError as e:
            p = gpt.submit_request(user_input)
            return p['choices'][0]['text']




@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
    '''This will take conversation id and conversations and dump them to last_conversation to update the responses.jsonl to improve the chatbot efficiency'''
    data = request.json
    id = data["id"]
    messages = data["messages"]
    try:
        conv_id = (open("last_conversation_id.txt").read())
    except FileNotFoundError as e:
        open("last_conversation_id.txt","w").write(str(id))
        conv_id = (open("last_conversation_id.txt").read())
    if conv_id == id:
        open("last_conversation.json","w").write(messages)
    else:
        open("last_conversation_id.txt","w").write(str(id))
        open("last_conversation.json", "w").write(messages)
    return "ok"

@app.route('/get_conversation_id', methods=['GET'])
def get_conversation_id():
    '''This will read the conversation ID from a file and return it as a response.'''
    conv_id = open("last_conversation_id.txt").read()
    return conv_id
if __name__ == '__main__':
    app.run(debug=True)