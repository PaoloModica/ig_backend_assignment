from server.flask_server import app, init_server

if __name__ == '__main__':
    init_server()
    app.run(debug=False, host='0.0.0.0', port=8080)