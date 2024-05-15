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
bp = Blueprint('ingredient', __name__, url_prefix='/')

@bp.route('/ingredients', methods=['POST'])

def record():
    try:
        db = get_db()
        ingredientId = str(uuid.uuid4())
        data = request.json

        userId = data.get('userID')
        ingredientName = data.get('ingredientName')
        unit =  data.get('unit')

        logger.info('POST ingredient')
        db.execute(
            "INSERT INTO ingredient (id, userID, ingredient_name,unit) VALUES (?,?,?,?)",(ingredientId, userId, ingredientName, unit)
        )
        db.commit()
        return jsonify({'message': 'Ingredient added successfully'}), 200

    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500


@bp.route('/ingredients', methods=['GET'])   
def search():
    db = get_db()
    keyword = request.args.get('search')
    if keyword:  
        query = """
        SELECT * FROM ingredient
        WHERE ingredient_name LIKE ?
        """
        searchTerm = f"%{keyword}%"
        ingredients = db.execute(query, (searchTerm,)).fetchall()
      
        ingredient_json = []
        for ingredient in ingredients:
            print(ingredient)
            ingredient_json.append({
                'id': ingredient[0],
                'userId': ingredient[1],
                'ingredientName': ingredient[2],
                'unit': ingredient[3],
            })
        return jsonify(ingredient_json)
    else:
        queryResult = "Ingredients not found, please use external resource"
        return jsonify([])


@bp.route('/ingredients/<ingredient_id>', methods=['DELETE'])
def delete(ingredient_id):
    try:
        db = get_db()
        logger.info(f"Fetching ingredient detail for ingredient ID: {ingredient_id}")
        check_query = 'SELECT COUNT(*) FROM ingredient where id = ?'
        check_result = db.execute(check_query,(ingredient_id,)).fetchone()

        if check_result[0] == 0:
            return jsonify({'error': 'Ingredient not found in the ingredient table'}), 404
        
        else:
            logger.info('Delete method')
            query = 'DELETE FROM ingredient WHERE id = ?'
            db.execute(query, (ingredient_id,))
            db.commit()
            return jsonify({'message':'This ingredient has been deleted successfully'})
    except Exception as e:
        logger.error(f"Error occurred while processing the delete ingredient:{str(e)}")
        return jsonify({'error': 'Could not delete ingredient'}), 500