from flask import Flask, render_template, Blueprint, jsonify, request
from .database import db, GGoals
from datetime import datetime
from flask_login import login_required, current_user

goals = Blueprint('goals', __name__)

Goals = []

@goals.route('/savegoals', methods=['POST'])
@login_required
def SaveGoals():
    data = request.get_json()
    tm = data.get('timeachieve')
    tm_ = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
    goals_table = GGoals(
        your_goals=data.get('goalss'),
        session=data.get('session'),
        time_to_achieve_goals=tm_,
        user_id=current_user.id
    )
    db.session.add(goals_table)
    db.session.commit()

    # print(f"Task added for {date}: {task}")
    return jsonify({'status': 'success', 'message': 'Task added successfully'}), 200

if __name__ == '__main__':
    goals.run(debug=True)