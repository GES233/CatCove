import os
from pprint import pprint
from catcove import create_app

os.environ["APP_ENV"] = "dev"

app = create_app()
if app.config["ENV"] == "dev":
    print("App configure mode: dev.")
    print("Routers:")
    pprint(app.router.routes_all)
    print("--------")
    print("Context:")
    pprint(app.ctx)
    print("========")

app.run(
    host="127.0.0.1",
    # host="0.0.0.0",  # `route print`
    port="6969",
    dev=True,
    workers=1
)
