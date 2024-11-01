from flask import Blueprint, abort, request, jsonify, render_template, flash, redirect, url_for
from app.models import Ghosts, db
from app.routes import admin_required
from flask_login import login_required

api = Blueprint('api', __name__, url_prefix='/api/ghosts')

#Admin routes
@api.route('/', methods=['POST'])
@admin_required
def add_ghost():
    if request.method == 'POST':
        ghost_name = request.form.get('ghost_name')
        description = request.form.get('description')
        power_level = request.form.get('power_level')
        status = request.form.get('status', 'not captured')
        special_abilities = request.form.get('special_abilities')
        picture_url = request.form.get('picture_url')
        api_endpoint = request.form.get('api_endpoint')

        new_ghost = Ghosts(
            ghost_name=ghost_name,
            description=description,
            power_level=int(power_level),
            status=status,
            special_abilities=special_abilities,
            picture_url=picture_url,
            api_endpoint=api_endpoint
        )
        power_level = int(power_level)

        db.session.add(new_ghost)
        db.session.commit()

        flash("New ghost added successfully!", "success")
        return redirect(url_for('VirtualEctoContainmentUnit'))
    return render_template('add_ghost.html')

@api.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_ghost(id):
    ghost = Ghosts.query.get_or_404(id)
    db.session.delete(ghost)
    db.session.commit()
    return jsonify({"message":"Ghost deleted successfully"}), 200

@api.route('/<int:id>', methods=['PUT'])
@admin_required
def update_ghost(id):
    data = request.get_json()
    ghost = Ghosts.query.get_or_404(id)
    ghost.ghost_name = data.get('ghost_name', ghost.ghost_name)
    ghost.description = data.get('description', ghost.description)
    ghost.power_level = data.get('power_level', ghost.power_level)
    ghost.status = data.get('status', ghost.status)
    ghost.special_abilities = data.get('special_abilities', ghost.special_abilities)
    ghost.picture_url = data.get('picture_url', ghost.picture_url)
    db.session.commit()
    return jsonify({"message":"Ghost updated successfully"}), 200


#Public routes
@api.route('/public/<identifier>', methods=(['GET']))
def get_ghost(identifier):
    if identifier.isdigit():
        ghost = Ghosts.query.get_or_404(int(identifier))
    else: 
        ghost = Ghosts.query.filter_by(ghost_name=identifier).first_or_404()
    return render_template('ghost_detail.html', ghost=ghost)

@api.route('/public/by_endpoint', methods=['GET'])
def get_ghost_by_api():
    api_endpoint = request.args.get('api_endpoint')
    if not api_endpoint:
        return jsonify({"error": "api_endpoint parameter is required"}), 400
    
    ghost = Ghosts.query.filter_by(api_endpoint=api_endpoint).first_or_404()
    return jsonify({
        "id": ghost.id,
        "ghost_name": ghost.ghost_name,
        "description": ghost.description,
        "power_level": ghost.power_level,
        "status": ghost.status,
        "special_abilities": ghost.special_abilities,
        "picture_url": ghost.picture_url,
        "api_endpoint": ghost.api_endpoint
        }), 200

@api.route('/public/ghost/<int:ghost_id>', methods=['GET'])
def ghost_detail(ghost_id):
    ghost = Ghosts.query.get_or_404(ghost_id)
    return render_template('ghost_detail.html', ghost=ghost)

@api.route('/public/<int:id>/capture', methods=['POST'])
@login_required
def capture_ghost(id):
    ghost = Ghosts.query.get_or_404(id)
    if ghost.status == 'captured':
        return jsonify({"message": "Ghost already captured"}), 400
    ghost.status = 'captured'
    ghost.captured_by = current_user.id 
    db.session.commit()
    return jsonify({"message": f"{ghost.ghost_name} has been captured!"}), 200

@api.route('/public/<int:id>', methods=['GET'])
def get_ghost_by_id(id):
    ghost = Ghosts.query.get_or_404(id)
    return jsonify({
        "id": ghost.id,
        "ghost_name": ghost.ghost_name,
        "description": ghost.description,
        "power_level": ghost.power_level,
        "status": ghost.status,
        "special_abilities": ghost.special_abilities,
        "picture_url": ghost.picture_url,
        "api_endpoint": ghost.api_endpoint
    }), 200

@api.route('/public/all', methods=['GET'])
def get_all_ghosts():
    ghosts = Ghosts.query.all()
    return jsonify([
        {
            "id": ghost.id,
            "ghost_name": ghost.ghost_name,
            "description": ghost.description,
            "power_level": ghost.power_level,
            "status": ghost.status,
            "special_abilities": ghost.special_abilities,
            "picture_url": ghost.picture_url,
            "api_endpoint": ghost.api_endpoint
        }
        for ghost in ghosts
    ]), 200
