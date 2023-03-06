import openai
import os
import json
import shutil

filename = "static/_conversation_history.json"
init_filename = "static/_conversation_history_init.json"

openai.api_key = os.environ['OPENAI_API_KEY']


class ChatBot:
    def __init__(self):
        if not os.path.isfile(filename):
            shutil.copyfile(init_filename, filename)
            with open(filename, "r") as file:
                content = file.read()
            self.messages = json.loads(content)
        else:
            # read json file as a dictionary
            with open(filename, "r") as file:
                content = file.read()
            self.messages = json.loads(content)

    def __call__(self, message):
        # read existing conversation history into messages
        with open(filename, "r") as file:
            content = file.read()
        self.messages = json.loads(content)
        # add user message to conversation history
        self.messages.append({"role": "user", "content": message})
        # overwrite conversation history file with updated messages
        with open(filename, 'w') as f:
            json.dump(self.messages, f, indent=4)
        # get response from OpenAI GPT-3 API
        result = self.execute()
        # add AI response to conversation history
        self.messages.append({"role": "assistant", "content": result})
        # overwrite conversation history file with updated messages
        with open(filename, 'w') as f:
            json.dump(self.messages, f, indent=4)
        return result


def execute(self):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=self.messages)
    return completion.choices[0].message.content
