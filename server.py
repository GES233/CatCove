import os
from pprint import pprint
from catcove import create_app

os.environ["APP_ENV"] = "dev"

app = create_app()
pprint(app.router.routes_all)
app.run(dev=True)
