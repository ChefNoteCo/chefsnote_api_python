import uuid
from datetime import date
from flask import jsonify
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Define blueprint
bp = Blueprint('recipe', __name__, url_prefix='/recipe')

# Define route to handle form submission
@bp.route('/record', methods=('GET', 'POST'))
@login_required
def record():
    if request.method == "POST":
        # Retrieve form data
        recipeName = request.form['recipeName']
        prepTime = request.form['prepTime']
        cookTime = request.form['cookTime']
        servings = request.form['servings']
        # Generate unique ID for each record
        unique_id = str(uuid.uuid4())
        version = unique_id + "#" + str(date.today())
        # Log form data
        logger.info(f"Form Data - ID: {unique_id}, Recipe Name: {recipeName}, Prep Time: {prepTime}, Cook Time: {cookTime}, Servings: {servings}")
        error = None

        # Validate form data
        if not recipeName:
            error = 'Recipe Name is required.'
        elif not prepTime:
            error = 'Prep Time is required.'
        elif not cookTime:
            error = 'Cook Time is required.'
        elif not servings:
            error = 'Number of servings is required.'

        # If no validation errors, insert record into database
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO recipes (id, version, name, prepTime, cookTime, servings) VALUES (?, ?, ?, ?, ?, ?)",
                (unique_id, version, recipeName, prepTime, cookTime, servings),
            )
            db.commit()
            flash('Recipe added successfully.')
            return redirect(url_for('recipe.record'))
        
    # Render the form template for GET requests and POST requests with errors
    return render_template('recipe/recipe_record.html')

@bp.route('/allrecipes', methods=('GET',)) 
def all_recipes():
    db = get_db()
    recipes = db.execute("SELECT * FROM recipes").fetchall()
    
    # Convert the list of recipe dictionaries to a list of JSON objects
    recipe_json = [] 
    for recipe in recipes:
        recipe_json.append({
            'id': recipe['id'],
            'version':recipe['version'],
            'name': recipe['name'],
            'prepTime': recipe['prepTime'],
            'cookTime': recipe['cookTime'],
            'servings': recipe['servings'],
            # Add other fields as needed
        })
    
    # Return the list of recipes as JSON
    return jsonify(recipes=recipe_json)