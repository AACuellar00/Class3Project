from src import create_app
from prometheus_flask_exporter import PrometheusMetrics

app = create_app()
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

if __name__ == '__app__':
    app.run(debug=True)
