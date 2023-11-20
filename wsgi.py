from app import init_app

app = init_app()

if __name__ == "__main__":
    # Run this web app in the debug mode.
    # The debug mode can test the code changes of the server-side module. If there is any edit, the server will be restarted automatically
    app.run(host="0.0.0.0", port=8183, debug=True)
