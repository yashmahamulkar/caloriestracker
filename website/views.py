from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .models import CalorieEntry
from . import db


views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    entries_data = []
    
    if request.method == 'POST':
        date = request.form.get('date')
        calories = int(request.form.get('calories'))

        existing_entry = CalorieEntry.query.filter_by(user_id=current_user.id, date=date).first()

        if existing_entry:
      
            existing_entry.calories += calories
        else:
      
            new_entry = CalorieEntry(date=date, calories=calories, user=current_user)
            db.session.add(new_entry)

        db.session.commit()

        flash('Calorie entry added/updated successfully!', category='success')


    entries = CalorieEntry.query.filter_by(user_id=current_user.id).all()

  
    entries_data = [{'date': entry.date, 'calories': entry.calories} for entry in entries]

    return render_template("home.html", user=current_user, entries_data=entries_data)
