import os
from catcove import create_app

os.environ["APP_ENV"] = "dev"

app = create_app()
app.run(dev=True)
