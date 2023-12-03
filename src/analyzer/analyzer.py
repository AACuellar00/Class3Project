from src.analyzer import create_app

app = create_app()

if __name__ == '__analyzer__':
    app.run(port=5002)