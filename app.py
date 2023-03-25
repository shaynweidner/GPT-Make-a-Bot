from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from chatbot import ChatBot  # importing class ChatBot from module chatbot
import shutil  # importing shutil module of python used to operate with file and directories
import os  # importing os module of python used to perform various operating system-related operations
import json  # importing json module of python used to read and write json files

app = Flask(__name__)  # app instance is created
CORS(app)


# Route decorator, it routes URL function to /super_secret_slug endpoint
@app.route('/', methods=["GET"])
def index():
    # It's rendering index.html template on host with local variable
    return render_template('index.html', **locals())


# Route decorator, it routes URL function to '/chatbot' endpoint
@app.route('/chatbot', methods=["POST"])
def chatbotResponse():
    # if condition if it's HTTP request method is POST.
    if request.method == 'POST':
        # Parsing the user's message parameter from JSON request data
        user_message = request.json['question']
        # passing the user's message as an argument to the `chatterbox` object and storing returned response in response
        response = chatterbox(user_message)
        # It converts the given dictionary type argument into json string format.
        return jsonify({"response": response})


# Route decorator, it routes URL function to '/erase_chatbot' endpoint
@app.route('/erase_chatbot', methods=["POST"])
def erase_chatbot():
    # Checking if _conversation_history.json file exists
    if os.path.isfile('static/_conversation_history.json'):
        # using unlink() from os module to delete file permanently
        os.unlink('static/_conversation_history.json')
        # Copying the content of source to destination file
        shutil.copyfile('static/_conversation_history_init.json',
                        'static/_conversation_history.json')
    chatterbox = ChatBot()  # Just to initialize and re-set the conversation history
    return jsonify({})  # returning empty dictionary format response


# Route decorator, it routes URL function to '/reinitialize_chatbot' endpoint
@app.route('/reinitialize_chatbot', methods=["POST"])
def reinit_chatbot():
    # copying the previous state of chatbot history
    shutil.copyfile('static/_conversation_history_init.json',
                    'static/_conversation_history.json')
    # rebuilding the chatbot by calling the constructor.
    chatterbox = ChatBot()
    return jsonify({})  # returning empty dictionary format response

# Serve _conversation_history_init.json
@app.route('/serve_init_json', methods=["GET"])
def serve_init_json():
    with open('static/_conversation_history_init.json', 'r') as f:
        init_json = json.load(f)
    response = jsonify(init_json)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Serve _conversation_history.json
@app.route('/serve_json', methods=["GET"])
def serve_json():
    with open('static/_conversation_history.json', 'r') as f:
        the_json = json.load(f)
    response = jsonify(the_json)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



# Drop last message from _conversation_history.json
@app.route('/drop_last_message', methods=["POST"])
def drop_last_message():
    print("dropping last message")
    with open('static/_conversation_history.json', 'r') as f:
        the_json = json.load(f) 
    # if last message is has role of "system", then do nothing
    if the_json[-1]["role"] == "system":
        print("can't drop last message.  It is the system prompt message.")
        return(jsonify({"response": "last message is a system message"}))
    # if last message has any other role, then remove it
    trimmed_json = the_json[:-1]
    with open('static/_conversation_history.json', 'w') as f:
        json.dump(trimmed_json, f, indent=4)
    return(jsonify({"response": "removed last message"}))

# Change chat target
@app.route('/change_chat_target/', methods=["POST"])
def change_chat_target():
    print("changing chat target")
    target_bot = request.json['target_bot']
    current_bot = get_current_bot()
    # save _conversation_history.json as _conversation_history.json.$current_bot
    with open('static/_conversation_history.json', 'r') as f:
        the_json = json.load(f)
    with open('static/_conversation_history.json' + current_bot, 'w') as f:
        json.dump(the_json, f, indent=4)
    # save _conversation_hsitory_init.json as _conversation_history_init.json.$current_bot
    with open('static/_conversation_history_init.json', 'r') as f:
        the_json_init = json.load(f)
    with open('static/_conversation_history_init.json' + current_bot, 'w') as f:
        json.dump(the_json_init, f, indent=4)
    
    # now we copy _conversation_history_init.json$target_bot to _conversation_history_init.json
    with open('static/_conversation_history_init.json' + target_bot, 'r') as f:
        the_json_init_target = json.load(f)
    with open('static/_conversation_history_init.json') as f:
        json.dump(the_json_init_target, f, indent=4)
    # now we copy _conversation_history.json$target_bot to _conversation_history.json
    with open('static/_conversation_history.json' + target_bot, 'r') as f:
        the_json_target = json.load(f)
    with open('static/_conversation_history.json') as f:
        json.dump(the_json_target, f, indent=4)
    print("target should have changed from " + current_bot + " to " + target_bot)
    return(jsonify({"response": "changed chat target to " + target_bot}))

# a bit hacky, sorry
@app.route('/get_current_bot/', methods=["GET"])
def get_current_bot():
    with open('static/current_bot.txt', 'r') as f:
        current_bot = f.readlines()[0]
    print(current_bot)
    return(jsonify({"current_bot": current_bot}))


if __name__ == '__main__':
    # creating instance of Class ChatBot and storing it in chatterbox variable.
    chatterbox = ChatBot()
    # Running a Flask Application listening at IP address 0.0.0.0 over port number 8888 with debug mode on and disabling reloading.
    app.run(host='0.0.0.0', port='8888', debug=True, use_reloader=False)
