import os
from catcove import create_app

os.environ["APP_ENV"] = "dev"

app = create_app()
app.run(
    host="127.0.0.1",
    # host="0.0.0.0",  # `route print`
    port="6969",
    dev=True
)
