from app import app

# use this file to start the server instead of running app.py directly
# binds to 0.0.0.0 so it's reachable from other devices on the network, not just localhost
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
