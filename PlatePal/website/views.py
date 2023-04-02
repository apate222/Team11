from flask import Blueprint, render_template, request, flash, jsonify, Flask, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .forms import createRecipeForm
from .models import Recipe, User


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # if request.method == 'POST':
    # note = request.form.get('note')#Gets the note from the HTML

    # if len(note) < 1:
    #    flash('Note is too short!', category='error')
    # else:
    #    new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
    #    db.session.add(new_note) #adding the note to the database
    #    db.session.commit()
    #    flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    user = current_user
    user_recipes = Recipe.query.filter_by(user_id=user.id).all()
    return render_template("user.html", user=user, user_recipes=user_recipes)


@views.route('/createRecipe', methods=['GET', 'POST'])
@login_required
def createRecipe():
    form = createRecipeForm()

    if form.validate_on_submit():
        recipe = Recipe(user_id=current_user.id,
                        title=form.title.data,
                        description=form.description.data,
                        servings=form.servings.data,
                        prep_time=form.prep_time.data,
                        cook_time=form.cook_time.data)
        db.session.add(recipe)
        db.session.commit()

        flash('Recipe created successfully!', 'success')
        return redirect(url_for('views.user', user=current_user))

    return render_template('createRecipe.html', title='Create Recipe', form=form, user=current_user)

@views.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    return render_template("about.html", user=current_user)