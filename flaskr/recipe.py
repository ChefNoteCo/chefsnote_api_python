import uuid
from datetime import date
from flask import (
    Blueprint, request, jsonify
)
from flaskr.db import get_db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define blueprint
bp = Blueprint('recipe', __name__, url_prefix='/')

#Get all recipes
@bp.route('/recipes', methods=('GET',)) 
def get_all_recipes():
    try:
        logger.info(f"Fetching recipe details for all recipe")
        db = get_db()
        logger.info('GET method')
        recipes = db.execute("SELECT * FROM recipes WHERE isLatestVersion=?",('True',)).fetchall()
    
        # Convert the list of recipe dictionaries to a list of JSON objects
        recipe_json = [] 
        for recipe in recipes:
            recipe_json.append({
            'id': recipe['id'],
            'parentId': recipe['parent_id'],
            'name': recipe['recipe_name'],
            'prepTime': recipe['prepTime'],
            'cookTime': recipe['cookTime'],
            'servings': recipe['servings'],
            'prepNote': recipe['prep_notes'],
        })
    
        # Return the list of recipes as JSON
        return jsonify(recipes=recipe_json)
    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# A single recipe
@bp.route('/recipes/<string:recipe_id>',methods=["GET"])    
def get_single_recipe(recipe_id):
    try:
        logger.info(f"Fetching recipe details for recipe ID: {recipe_id}")
        db = get_db()
        logger.info('GET method')
        recipe = db.execute(
            'SELECT * FROM recipes WHERE WHERE id =?',(recipe_id,)).fetchone()

        if recipe is None:
            logger.info('No recipe found')
            return jsonify({"error": "Recipe not found"}), 404
        logger.info('Recipe found')
        return jsonify(recipe), 200
    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# Add version recipe
@bp.route('/recipes/<string:recipe_id>',methods=["PUT"])    
def put_single_recipe(recipe_id):
    try:
        logger.info(f"Add recipe details for recipe ID: {recipe_id}")

        data = request.json
        id = data.get('id')
        recipeName = data.get('recipeName')
        prepTime = data.get('prepTime')
        cookTime = data.get('cookTime')
        servings = data.get('servings')
        prepNotes = data.get('prepNotes')
        instruction = data.get('instruction')
        ingredients = data.get('ingredient',[])

        # Parse id to create a new version
        try: 
            parseVersionId = id.split('#')[0]
        except IndexError:
            parseVersionId = id
        
        recipeVersionID = parseVersionId + "#" + str(date.today())

        db = get_db()
        logger.info('PUT method')
        db.execute("BEGIN TRANSACTION")
        
        # Insert the new recipe to recipe table, since this is a version, parent_id is the ID before parse, and id and child_id are the same
        db.execute(
            "UPDATE recipes SET child_id=?, isLatestVersion=? WHERE id=?",(recipeVersionID, "False", id),
        )
        db.execute(
            "INSERT INTO recipes (id, parent_id, child_id, recipe_name, prepTime, cookTime, servings, prep_notes, instruction, isLatestVersion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (recipeVersionID, id, recipeVersionID, recipeName, prepTime, cookTime, servings, prepNotes, instruction, "True"),
        )

        # Insert the new recipe to recipe_ingredient table
        for ingredient in ingredients:
            ingredientId = ingredient.get('ingredientId')
            userId = ingredient.get('userId')
            externalId = ingredient.get('externalId')
            measurement = ingredient.get('measurement')
            unit = ingredient.get('unit')

            db.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id,user_id,external_id, measurement,unit) VALUES (?,?,?,?,?,?)", (recipeVersionID, ingredientId, userId, externalId, measurement, unit),
            )
        
        db.commit()
        return jsonify({'message': 'Recipe added successfully'}), 201
    
    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

#Add newly create recipe
@bp.route('/recipes', methods=('POST',))
def record():
    try:
        logger.info(f"Add new recipe details for a recipe")
        data = request.json
    
        recipeName = data.get('recipeName')
        prepTime = data.get('prepTime')
        cookTime = data.get('cookTime')
        servings = data.get('servings')
        prepNotes = data.get('prepNotes')
        instruction = data.get('instruction')
        ingredients = data.get('ingredient',[])
        recipeVersionID = str(uuid.uuid4()) + "#" + str(date.today())

        db = get_db()
        logger.info('POST method')
        db.execute("BEGIN TRANSACTION")
        # Insert the new recipe to recipe table
        db.execute(
            "INSERT INTO recipes (id, parent_id, child_id, recipe_name, prepTime, cookTime, servings, prep_notes, instruction, isLatestVersion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(recipeVersionID, recipeVersionID, recipeVersionID, recipeName, prepTime, cookTime, servings, prepNotes, instruction, 'True'),
        )
    
        # Insert the new recipe to recipe_ingredient table
        for ingredient in ingredients:
            ingredientId = ingredient.get('ingredientId')
            userId = ingredient.get('userId')
            externalId = ingredient.get('externalId')
            measurement = ingredient.get('measurement')
            unit = ingredient.get('unit')

            db.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id,user_id,external_id, measurement,unit) VALUES (?,?,?,?,?,?)", (recipeVersionID, ingredientId, userId, externalId, measurement, unit),)
        
            db.commit()

            return jsonify({'message': 'Recipe added successfully'}), 201
    
    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# Delete recipe
@bp.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        logger.info(f"Fetching recipe details for recipe ID: {recipe_id}")
        db = get_db()
        logger.info('Delete method')
        db.execute("BEGIN TRANSACTION")
        db.execute(
            'DELETE FROM recipe_ingredients WHERE recipe_id = ?',(recipe_id,)
        )
        db.execute(
            'DELETE FROM recipes WHERE id = ?', (recipe_id,)
        )
        db.commit()
        return jsonify({'message':'This recipe has been deleted successfully'})
    except Exception as e:
        logger.error(f"Error occurred while processing the delete: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500


# Add feedback
@bp.route('/recipes/<string:recipe_id>',methods=["PATCH"])
def add_feedback(recipe_id):
    try:
        logger.info(f"Fetching recipe details for recipe ID: {recipe_id}")
        db = get_db()
        logger.info('Get Feedback method')
        data = request.json
        feedback = data.get('feedbackNotes')

        db.execute("BEGIN TRANSACTION")
        existing_feedback = db.execute(
            'SELECT feedback_notes FROM recipe WHERE id = ?',(recipe_id,)
        ).fetchone().split(',')
        
        existing_feedback.append(feedback)
        update_feedback = ",".join(existing_feedback)
        db.execute(
            'UPDATE recipes SET feedback_notes = ? WHERE id = ?', (update_feedback,recipe_id)
        )
        db.commit()
        return jsonify({'message':'The new feedback note has been added to the recipe successfully'})
    except Exception as e:
        logger.error(f"Error occurred while processing adding feedback: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500
