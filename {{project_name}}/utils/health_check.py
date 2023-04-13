from http.server import BaseHTTPRequestHandler, HTTPServer


# todo
class HealthServer(BaseHTTPRequestHandler):
    """Small webserver to serve scheduler health check"""

    def do_GET(self):
        if self.path == '/health':
            try:
                scheduler_job = None
                if scheduler_job and scheduler_job.is_alive():
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_error(503)
            except Exception:
                self.send_error(503)
        else:
            self.send_error(404)


def serve_health_check():
    health_check_port = 9000
    httpd = HTTPServer(("0.0.0.0", health_check_port), HealthServer)
    httpd.serve_forever()