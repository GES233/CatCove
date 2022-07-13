from catcove import app_with_env_mode
import os

if __name__ == "__main__":
    app = app_with_env_mode()
    if app.config.ENV == "dev":
        app.run(
            port="6699",
            host="localhost",
            dev=True,
            debug=True,
            auto_reload=True,
            )
    else:
        app.run(
            host="0.0.0.0",
            port="6969",
            workers=4,
            access_log=False
        )