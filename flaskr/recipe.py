import uuid
from datetime import date
from flask import (
    Blueprint, flash, g, redirect, render_template, request, jsonify, session, url_for
)
from flaskr.db import get_db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Define blueprint
bp = Blueprint('recipe', __name__, url_prefix='/recipe')

#Add newly create recipe
@bp.route('/record', methods=('POST',))
def record():
    data = request.json
    id = data.get('id')
    recipeName = data.get('recipeName')
    prepTime = data.get('prepTime')
    cookTime = data.get('cookTime')
    servings = data.get('servings')
    prepNotes = data.get('prepNotes')
    instruction = data.get('instruction')
    parentId = data.get('parentId')
    ingredients = data.get('ingredient',[])
    
    # check if the recipe from form is a newly create recipe
    if id is None:
        recipeVersionID = str(uuid.uuid4()) 
    else:
        recipeVersionID = parentId + "#" + str(date.today())

    db = get_db()
    db.execute("BEGIN TRANSACTION")
        # Insert the new recipe to recipe table

    db.execute(
        "INSERT INTO recipes (id, parent_id, child_id, recipe_name, prepTime, cookTime, servings, prep_notes, instruction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(recipeVersionID, recipeVersionID, recipeVersionID, recipeName, prepTime, cookTime, servings, prepNotes, instruction),
            )
    
    
    # Insert the new recipe to recipe_ingredient table
    for ingredient in ingredients:
        ingredientId = ingredient.get('ingredientId')
        userId = ingredient.get('userId')
        externalId = ingredient.get('externalId')
        measurement = ingredient.get('measurement')
        unit = ingredient.get('unit')
        db.execute(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id,user_id,external_id, measurement,unit) VALUES (?,?,?,?,?,?,?)", (recipeVersionID, ingredientId, userId, externalId, measurement, unit),)
    
    db.commit()

    return jsonify({'message': 'Recipe added successfully'}), 201

#Get all recipes
@bp.route('/allrecipes', methods=('GET',)) 
def all_recipes():
    db = get_db()
    recipes = db.execute("SELECT * FROM recipes").fetchall()
    
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
            'servings': recipe['feedback_notes'],
            'prepNote': recipe['prep_notes'],
            'instruction': recipe['instruction'],
        })
    
    # Return the list of recipes as JSON
    return jsonify(recipes=recipe_json)

#Record a new version of the existing recipes  
@bp.route('/version_record', methods=('POST',))
def version_record():
    data = request.json
    id = data.get('id')
    recipeName = data.get('recipeName')
    prepTime = data.get('prepTime')
    cookTime = data.get('cookTime')
    servings = data.get('servings')
    feedbackNotes = data.get('feedbackNotes')
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

   
    db.execute("BEGIN TRANSACTION")
    
    # Insert the new recipe to recipe table, since this is a version, parent_id is the ID before parse, and id and child_id are the same
    db.execute(
        "INSERT INTO recipes (id, parent_id, child_id, recipe_name, prepTime, cookTime, servings, prep_notes, instruction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(recipeVersionID, id, recipeVersionID, recipeName, prepTime, cookTime, servings, prepNotes, instruction),
    )
    
    
    # Insert the new recipe to recipe_ingredient table
    for ingredient in ingredients:
        ingredientId = ingredient.get('ingredientId')
        userId = ingredient.get('userId')
        externalId = ingredient.get('externalId')
        measurement = ingredient.get('measurement')
        unit = ingredient.get('unit')
        db.execute(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id,user_id,external_id, measurement,unit) VALUES (?,?,?,?,?,?,?)", (recipeVersionID, ingredientId, userId, externalId, measurement, unit),
        )
    
    db.commit()
    return jsonify({'message': 'New version of the recipe added successfully'}), 201

# Get a single recipe
@bp.route('/recipe/<string:recipe_id>',methods=('GET','PUT'))    
def single_recipe(recipe_id):
    try:
        logger.info(f"Fetching recipe details for recipe ID: {recipe_id}")
        db = get_db()
        if request.method == 'GET':
            recipe = db.execute(
                'SELECT * FROM recipes WHERE WHERE id =?',(recipe_id,)).fetchone()

            if recipe is None:
                return jsonify({"error": "Recipe not found"}), 404
            return jsonify(recipe), 200

        elif request.method == "PUT":
            data = request.json
            id = data.get('id')
            recipeName = data.get('recipeName')
            prepTime = data.get('prepTime')
            cookTime = data.get('cookTime')
            servings = data.get('servings')
            feedbackNotes = data.get('feedbackNotes')
            prepNotes = data.get('prepNotes')
            instruction = data.get('instruction')
            ingredients = data.get('ingredient',[])
        
        db.execute("BEGIN TRANSACTION")
        
        # Insert the new recipe to recipe table, since this is a version, parent_id is the ID before parse, and id and child_id are the same
        db.execute(
            "INSERT INTO recipes (recipe_name, prepTime, cookTime, servings, prep_notes, instruction, feedback_notes) VALUES (?, ?, ?, ?, ?, ?, ?)",(recipeName, prepTime, cookTime, servings, prepNotes, instruction, feedbackNotes),
        )
        
        # Insert the new recipe to recipe_ingredient table
        for ingredient in ingredients:
            ingredientId = ingredient.get('ingredientId')
            userId = ingredient.get('userId')
            externalId = ingredient.get('externalId')
            measurement = ingredient.get('measurement')
            unit = ingredient.get('unit')
            db.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id,user_id,external_id, measurement,unit) VALUES (?,?,?,?,?,?,?)", (id, ingredientId, userId, externalId, measurement, unit),
            )
        
        db.commit()
    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500


