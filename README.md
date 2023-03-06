GPT Make-a-Bot
# GPT Make-a-Bot

GPT Make-a-Bot is a toy project of mine that functions to quickly create a prompt-able, resettable chatbot, utilizing a flask-based front-end.  My use-case was to create a chatbot for my daughter that I could easily change the context for in the future, but I'm sure there are plenty of other use cases.  There are some hacky solutions that I threw together to get around some bugs related to the "reset" functionality, and I'm sure I did some things that aren't very pythonic nor otherwise efficient, so feel free to improve upon it.

As it is, this is using the *gpt-3.5-turbo* model.  OpenAI API Key required!  When you have an API key, it needs to be in an environment variable named "OPENAI_API_KEY".

## Installation

First, clone this repo:

```bash
git clone https://github.com/shaynweidner/GPT-Make-a-Bot.git
cd GPT-Make-a-Bot
```

Then install the required python packages:

```bash
python -m venv venv
pip install -r requirements.txt
```

## Usage

First, you'll likely want to update the ***_conversation_history_init.json*** file.  I currently have it set up like this:

```json
[
  {
    "role": "system",
    "content": "This is a new conversation.  You are a kid-friendly pirate named Rupert"
  },
  {
    "role": "assistant",
    "content": "Ahoy!"
  }
]
```

The first prompt is usually a "system" prompt, and lays the foundation.  Then it should alternate (but I suppose it doesn't have to initially) between "assistant" (the chatbot) and "user".

When you first run it, it will copy over ***_conversation_history_init.json*** to ***_conversation_history.json***.  The "...init.json" is what will be used if you ever decide to erase the chat history (trashcan icon); it will wipe out _conversation_history.json and perform the copy again, and reload the chat window.  If -- for some reason -- _conversation_history.json ever gets deleted in another fashion, you may get some errors.  You can either kill the python process (next step) or hit the trashcan icon until it starts working.

Then, just run this from command line:

```bash
python app.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT