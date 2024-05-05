from flask import Flask
from src.libs.flask import create_flask_app

from .helpers import get_dummy_di, get_test_di

di = get_test_di()

# Clean cache
cache = di.cache.get_engine()
cache.flushdb()

# Clean database
print("Install Tables...")
di.persistence.drop_tables()
di.persistence.create_tables()

# Set APP
APP: Flask = create_flask_app(dependencies=di)

print("All registered routes:")
for rule in APP.url_map.iter_rules():
    print(f"{rule.endpoint:-<30} {rule.rule}")
print(" ----- ")

DUMMY_APP: Flask = create_flask_app(dependencies=get_dummy_di())
