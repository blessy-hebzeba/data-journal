from app import app

# @app is a decorator. A decorator modifies the function that follows it.
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"