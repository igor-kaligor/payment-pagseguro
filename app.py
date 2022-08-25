from flask import Flask

import routes
from settings import database, security

app = Flask(__name__)
db = database.init_app(app)
routes.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

