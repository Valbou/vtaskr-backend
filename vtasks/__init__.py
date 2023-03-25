from dotenv import load_dotenv

from .flask.main import create_flask_app


load_dotenv()

app = create_flask_app()
