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
    feedbackNotes = data.get('feedbackNotes')
    prepNotes = data.get('prepNotes')
    instruction = data.get('instruction')
    parentId = data.get('parentId')
    # check if the recipe from form is a newly create recipe
    if id is None:
        recipeVersionID = str(uuid.uuid4()) 
    else:
        recipeVersionID = parentId + "#" + str(date.today())


    logger.info(f"Data - ID: {recipeVersionID}, Recipe Name: {recipeName}, Prep Time: {prepTime}, Cook Time: {cookTime}, Servings: {servings}")
    
    db = get_db()

    # Insert the new recipe to recipe table
    db.execute(
        "INSERT INTO recipes (id, parent_id, child_id, recipe_name, prepTime, cookTime, servings, feedback_notes, prep_notes, instruction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(recipeVersionID, recipeVersionID, recipeVersionID, recipeName, prepTime, cookTime, servings, feedbackNotes, prepNotes, instruction),
            )
    db.commit()
    # Update the child_id of the parent
    db.execute(
        "UPDATE recipes set "
    )


   
    return jsonify({'message': 'Recipe added successfully'}), 201


#get all recipes
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
    
    # Parse id to create a new version
    try: 
        parseVersionId = id.split('#')[0]
    except IndexError:
        parseVersionId = id
    
    recipeVersionID = parseVersionId + "#" + str(date.today())

    logger.info(f"Data - ID: {recipeVersionID}, Recipe Name: {recipeName}, Prep Time: {prepTime}, Cook Time: {cookTime}, Servings: {servings}")
    
    db = get_db()
       # Update the child_id of the parent
    db.execute(
        "UPDATE recipes SET child_id = ? where id = ?" , (id,id)
    )
    db.commit()
    # Insert the new recipe to recipe table
    db.execute(
        "INSERT INTO recipes (id, parent_id, child_id, recipe_name, prepTime, cookTime, servings, feedback_notes, prep_notes, instruction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(recipeVersionID, id, recipeVersionID, recipeName, prepTime, cookTime, servings, feedbackNotes, prepNotes, instruction),
            )
    db.commit()
    

   
    return jsonify({'message': 'New version of the recipe added successfully'}), 201
