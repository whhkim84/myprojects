import re
import time
import threading

class Detector:
    def __init__(self):
        signatures = [
            'sqlmap', 'nikto', 'dirbuster', 'acunetix', 'fuzzer', 'curl',
            'masscan', 'wpscan', 'nmap', 'python-requests', 'libwww-perl'
        ]
        self.ua_regex = re.compile('|'.join(re.escape(s) for s in signatures), re.I)
        self.ip_stats = {}  # ip -> {'times': [ts,...], 'paths': set()}
        self.lock = threading.Lock()
        self.rate_window = 60
        self.max_requests = 20
        self.unique_paths_threshold = 10

    def analyze(self, req):
        ip = req.remote_addr or req.environ.get('HTTP_X_FORWARDED_FOR', 'unknown')
        ua = req.headers.get('User-Agent', '')
        detection_reasons = []
        detected = False

        if ua and self.ua_regex.search(ua):
            detected = True
            detection_reasons.append('User-Agent signature match')

        if not ua:
            detected = True
            detection_reasons.append('Missing User-Agent')

        accept = req.headers.get('Accept', '')
        if accept.strip() == '*/*' and ua and 'mozilla' not in ua.lower():
            detected = True
            detection_reasons.append('Generic Accept header */* with non-browser UA')

        now = time.time()
        with self.lock:
            stats = self.ip_stats.setdefault(ip, {'times': [], 'paths': set()})
            # prune old timestamps
            stats['times'] = [t for t in stats['times'] if now - t <= self.rate_window]
            stats['times'].append(now)
            stats['paths'].add(req.path)

            if len(stats['times']) > self.max_requests:
                detected = True
                detection_reasons.append('High request rate')

            if len(stats['paths']) > self.unique_paths_threshold:
                detected = True
                detection_reasons.append('Many unique paths requested')

        info = {
            'ip': ip,
            'ua': ua,
            'path': req.path,
            'method': req.method,
            'reasons': detection_reasons,
        }
        self._log(info, detected)
        return detected, detection_reasons

    def _log(self, info, detected):
        import json
        import logging
        logger = logging.getLogger('scanner_detector')
        try:
            logger.info(json.dumps({'detected': detected, **info}, ensure_ascii=False))
        except Exception:
            logger.info(str({'detected': detected, **info}))
