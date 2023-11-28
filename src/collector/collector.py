from src.collector import create_app

app = create_app()

if __name__ == '__collector__':
    app.run(debug=True, port=5001)
