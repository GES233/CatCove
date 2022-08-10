import os
from pprint import pprint
from catcove import create_app

os.environ["APP_ENV"] = "dev"

app = create_app()
pprint(app.router.routes_all)
app.run(
    # host="0.0.0.0",  # `route print`
    # port="6969",
    dev=True
)
