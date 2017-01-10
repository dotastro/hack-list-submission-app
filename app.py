import os
from hack_submission.webapp import app

port = int(os.environ.get('PORT', 5000))
debug = bool(os.environ.get('DEBUG', False))
host = os.environ.get('HOST', None)
app.run(host=host, debug=debug, port=port)
