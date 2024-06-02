# Persuasion Simulator

A final project for CST1000 at Westlake University. (2024 Spring)

This is a chat application built with Flask and MongoDB. It allows users to register, log in, send messages, and interact with a chatbot.

## Features

- User registration and login
- Message sending between users
- Interaction with a chatbot
- Storage and retrieval of chat history

## Installation (For Direct use)
### Create a virtual environment
```
conda create -n Persuasion python=3.10
conda activate Persuasion
```
### Install packages
```
bash environment.sh (linux)
pip install -r requirements.txt (windows/linux)
```
## Usage

### Direct use

First, you need to start the MongoDB server. Then, you can start the Flask server with the following command:

```bash
python website.py
```
The application will run on port 5000 by default.

To use the application, open your browser and visit http://localhost:5000. You will see the main interface of the application. You can register a new user and log in with this user. After logging in, you can send messages and see the responses from the chatbot.

### Docker Compose

1. Install Docker and Docker Compose.
2. Clone this repository.
3. Change [website.py](./website.py) from
```python
# Other code
app.config["MONGO_URI"] = "mongodb://localhost:27017/Test"
# Other code
if __name__ == '__main__':
    app.run(debug=True)
```
to
```python
# Other code
app.config["MONGO_URI"] = "mongodb://db:27017/Test"
# Other code
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
```
4. Run `docker-compose up` in the project directory.

The Flask application will be available at `http://localhost:5000`, and MongoDB will be available at `localhost:27017`.

## Gradio Tool for Analysis
We provide a tool based on Gradio in [Tools.py](./Tools.py) which helps you to do some sentiment analysis and gives you some suggested responses by the language model.

Before you run the Tools.py, you need to set your API:
```bash
export DASHSCOPE_API_KEY=YOUR_API
```

## Contributing

Contributions of all kinds are welcome! You can help us improve this project by submitting bug reports, suggesting improvements, or directly creating pull requests.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE file](./LICENSE) for details.
