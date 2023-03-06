from flask import Flask, render_template, jsonify, request
from chatbot import ChatBot  # importing class ChatBot from module chatbot
import shutil  # importing shutil module of python used to operate with file and directories
import os  # importing os module of python used to perform various operating system-related operations

app = Flask(__name__)  # app instance is created


# Route decorator, it routes URL function to /super_secret_slug endpoint
@app.route('/super_secret_slug', methods=["GET"])
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


if __name__ == '__main__':
    # creating instance of Class ChatBot and storing it in chatterbox variable.
    chatterbox = ChatBot()
    # Running a Flask Application listening at IP address 0.0.0.0 over port number 8888 with debug mode on and disabling reloading.
    app.run(host='0.0.0.0', port='8888', debug=True, use_reloader=False)
