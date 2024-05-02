Activate the environment
Before you work on your project, activate the corresponding environment:
$ . .venv/bin/activate

To run
$ flask --app flaskr run --debug

- Running on http://127.0.0.1:5000 (Press CTRL+C to quit)

Run the init-db command:

$ flask --app flaskr init-db
Initialized the database.
There will now be a flaskr.sqlite file in the instance folder in your project.

Note for Future ME :
http methods
Flask expects the methods argument to be a tuple, even if it only contains one method. eg @bp.route('/allrecipes', methods=('GET',))

TablePlus local database name : Chefsnote_database
