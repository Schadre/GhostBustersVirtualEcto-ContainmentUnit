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

        new_ghost = Ghosts(
            ghost_name=ghost_name,
            description=description,
            power_level=int(power_level),
            status=status,
            special_abilities=special_abilities,
            picture_url=picture_url
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
    return jsonify({"message":"Ghost deleted successfully"}, 200)

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
    return jsonify({"message":"Ghost updated successfully"}, 200)

@api.route('/<int:id>', methods=['GET'])
@admin_required
def get_ghost(id):
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

#Public routes
@api.route('/public', methods=['GET'])
def list_ghost():
    query = request.args.get('query', '').lower()
    filter_by = request.args.get('filter', 'name')

    if filter_by == 'name':
        ghosts = Ghosts.query.filter(Ghosts.ghost_name.ilike(f"%{query}%")).all()
    elif filter_by == 'number' and query.isdigit():
        ghosts = Ghosts.query.filter(Ghosts.id == int(query)).all()
    else:
        ghosts = Ghosts.query.all()

    return render_template('VirtualEcto-ContainmentUnit.html', ghosts=ghosts, query=query, filter_by=filter_by)

@api.route('/public/search', methods=['GET'])
def search_ghosts():
    query = request.args.get('query', '').lower()
    ghosts = Ghosts.query.filter(Ghosts.ghost_name.ilike(f"%{query}%")).all()
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

@api.route('/<int:id>/capture', methods=['POST'])
@login_required
def capture_ghost(id):
    ghost = Ghosts.query.get_or_404(id)
    if ghost.status == 'captured':
        return jsonify({"message": "Ghost already captured"}), 400
    ghost.status = 'captured'
    ghost.captured_by = current_user.id 
    db.session.commit()
    return jsonify({"message": f"{ghost.ghost_name} has been captured!"}), 200
