from src.collector import create_app

app = create_app()

if __name__ == '__app__':
    app.run(debug=True, port=5001)
