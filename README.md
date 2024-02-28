# ChatSCE

Chatbot API using the OpenAI API designed to help members within SCE with club and SJSU-related activities

# Usage

This is not an application and is designed to be integrated with another app

### Requirements

- `pip 24.0 or later`
- `Python 3.11 or later`

### Install Dependencies
- `pip install -r requirements.txt`

### Setup Environment Variables
- Create a .env file based on the dotenv_example
- IP is your local IP (0.0.0.0 can also be used; use localhost when accessing the API instead of the IP if using this method)
- Port number can be any port that isn't already occupied by another process

### Run
- `python ./main.py`
- Access API with localhost:[port_number]

### Unit Tests
- `pytest` or `python -m pytest` if pytest does not work
