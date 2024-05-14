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
Flask expects the methods argument to be a tuple, even if it only contains one method. eg @bp.route('/recipes', methods=('GET',))

TablePlus local database name : Chefsnote_database

Routes Explanation
GET /recipes - get all latest version of the recipe. Only query for the latest version, should the top level data not include ingredients
GET /recipes/:id (includes ingredients) - get a single recipe base on id
POST /recipes - to create new recipe and insert to table recipes and recipe_ingredients
PUT /recipes new recipe version - to create new version, and insert to table recipes and recipe_ingredients. Also update the child id in the previous version, change latest flag from true to false. new recipe also get flag as a latest version

DELETE /recipes/:id

GET /recipes/:id/feedback_notes
POST /recipes/:id/feedback_notes

DEBUG=0
INFO=1
WARN=2
ERROR=3
