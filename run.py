from catcove import create_app

if __name__ == "__main__":
    mode = "dev"
    app = create_app(mode)
    if mode == "dev":
        app.run(
            host="localhost",
            dev=True,
            debug=True,
            auto_reload=True,
            )
    else:
        app.run(
            host="0.0.0.0",
            port="9666",
            workers=4,
            access_log=False
        )