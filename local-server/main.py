from flask import Flask, request, g, Response
from flask_cors import CORS
import json
import uuid
from pkg import printer

app = Flask(__name__)
CORS(app)
app.debug = False

def log_request():
    data = {
        "id": g.request_id,
        "method": request.method,
        "path": request.path,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.get_json(silent=True),
        "remote_addr": request.remote_addr
    }
    print("→ Request:", json.dumps(data, indent=2, default=str))

def log_response(response: Response) -> Response:
    data = {
        "id": g.request_id,
        "status": response.status,
        "headers": dict(response.headers),
        "body": (response.get_data(as_text=True)[:500] + "...") if response.get_data() else ""
    }
    print("← Response:", json.dumps(data, indent=2, default=str))
    return response

@app.before_request
def before():
    g.request_id = uuid.uuid4().hex
    log_request()

@app.after_request
def after(response):
    return log_response(response)

@app.route('/echo', methods=['GET', 'POST'])
def echo():
    body = request.get_json(silent=True) or request.get_data(as_text=True)
    return {"you_sent": body}

@app.route('/print', methods=['POST'])
def _print():
    body = request.get_json(silent=True) or request.get_data(as_text=True)
    printer.print_jpg(body)
    return {"path": body}

if __name__ == '__main__':
    app.run(port=5000)
