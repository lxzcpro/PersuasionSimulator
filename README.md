# Persuasion Simulator

A final project for CST1000 in Westlake University. Not implement.

## Installation (For Direct use)
### Create a virtual environment
```
conda create -n Persuation python=3.10
conda activate Persuation
```
### Install packages
```
bash environment.sh  
```
## Usage

### Direct use

First, you need to start the MongoDB server. Then, you can start the Flask server with the following command:

```bash
python website.py
```
Now, you can access the simulator system in your browser at `http://localhost:5000`.

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

## Contributing

Contributions of all kinds are welcome! You can help us improve this project by submitting bug reports, suggesting improvements, or directly creating pull requests.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE file](./LICENSE) for details.
