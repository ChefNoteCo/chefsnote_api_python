Activate the environment
Before you work on your project, activate the corresponding environment:
$ . .venv/bin/activate

To run
$ flask --app hello run

- Serving Flask app 'hello'
- Running on http://127.0.0.1:5000 (Press CTRL+C to quit)

Don't forget to change flaskr directory to App directory this is just to follow the flask instruction

Initialize the Database File
Now that init-db has been registered with the app, it can be called using the flask command, similar to the run command from the previous page.

Note
If you’re still running the server from the previous page, you can either stop the server, or run this command in a new terminal. If you use a new terminal, remember to change to your project directory and activate the env as described in Installation.

Run the init-db command:

$ flask --app flaskr init-db
Initialized the database.
There will now be a flaskr.sqlite file in the instance folder in your project.

Random Note:
http methods
Flask expects the methods argument to be a tuple, even if it only contains one method. eg @bp.route('/allrecipes', methods=('GET',))
