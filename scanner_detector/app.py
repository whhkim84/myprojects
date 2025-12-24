import os
import logging
from flask import Flask, request, jsonify
from detector import Detector

app = Flask(__name__)
detector = Detector()

# log to repo/detections.log
base_dir = os.path.dirname(__file__)
log_path = os.path.abspath(os.path.join(base_dir, '..', 'detections.log'))
os.makedirs(os.path.dirname(log_path), exist_ok=True)

handler = logging.FileHandler(log_path)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger = logging.getLogger('scanner_detector')
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(handler)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'HEAD', 'OPTIONS'])
def handle(path):
    detected, reasons = detector.analyze(request)
    status = 403 if detected else 200
    body = {'scanner_detected': detected, 'reasons': reasons}
    return jsonify(body), status


if __name__ == '__main__':
    # allow overriding port with environment variable PORT
    try:
        port = int(os.environ.get('PORT', '8000'))
    except Exception:
        port = 8000
    app.run(host='0.0.0.0', port=port, debug=False)
