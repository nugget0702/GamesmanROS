import sqlite3
import requests
from flask import Flask, render_template, request, session, url_for, flash, redirect
from werkzeug.exceptions import abort

from util import (
    get_game_name,
    initialize_game,
    pick_best_position,
    achi_position_to_coord,
    connect4_position_to_coord,
)


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/games', methods=('POST',))
def games():
    return render_template('games.html')


@app.route('/variants', methods=('GET', 'POST'))
def variants():
    if request.method == 'POST':
        try:
            game_index = int(request.form['game_index'])
        except ValueError:
            flash("Invalid game index", "error")
            return redirect(url_for('index'))  # Redirect back to the index if there is an error
        
        session['game_index'] = game_index
        return redirect(url_for('variants', game_index=game_index))  # Redirect to the same page after POST
        
    # Handle GET request here
    game_index = request.args.get('game_index', type=int)
    if game_index:
        session['game_index'] = game_index
    return render_template('variants.html', post={"game_index": game_index})



@app.route('/handle', methods=['GET', 'POST'])
def handle():
    if request.method == 'POST':
        # Handle POST request
        try:
            variant_index = int(request.form['variant_index'])
            session['variant_index'] = variant_index
        except ValueError:
            flash("Invalid variant index", "error")
            return redirect(url_for('index'))

        data = {
            "content": "",
            "is_started": False,
        }
        return render_template('handle.html', post=data)
    
    # Handle GET request (optional, can provide default data or another page behavior)
    return render_template('handle.html', post={"content": "", "is_started": False})


@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        # Handle POST request (initialize game)
        game_index = session['game_index']
        variant_index = session['variant_index']
        static_URL, centers, starting_position, moves_data = initialize_game(game_index, variant_index)
        session['static_URL'] = static_URL
        session['centers'] = centers
        session['starting_position'] = starting_position
        session['moves_data'] = moves_data
        session['A_turn'] = True
        msg = f"Initialized game {get_game_name(game_index)} successfully!"
        session['start_message'] = msg
        
    return redirect(url_for('handle_started'))

@app.route('/handle_started', methods=['GET'])
def handle_started():
    msg = session.pop('start_message', "")
    data = {
        "content": msg,
        "is_started": True,
    }
    # Handle GET request (optional, can provide default data or page behavior)
    return render_template('handle.html', post=data)


@app.route('/move', methods=('POST',))
def move():
    data = {
        "content": "Game over",
        "is_started": False,
    }
    game_index = session['game_index']
    variant_index = session['variant_index']
    static_URL = session['static_URL']
    centers = session['centers']
    starting_position = session['starting_position']
    moves_data = session['moves_data']
    A_turn = session['A_turn']
    if game_index == 4:
        position_to_coord = achi_position_to_coord
    elif game_index == 16:
        position_to_coord = connect4_position_to_coord

    if len(moves_data) > 0:
        msg = ""
        error, new_position = pick_best_position(moves_data)
        if len(error) > 0:
            data['content'] = error
            return render_template('handle.html', post=data)
        error, move_coords = position_to_coord(starting_position, new_position, centers, variant_index)
        if len(error) > 0:
            data['content'] = error
            return render_template('handle.html', post=data)

        msg += f"starting position: {starting_position}\n"
        msg += f"new position: {new_position}\n"
        if A_turn:
            msg += f"A : {move_coords}\n"
            session['A_turn'] = False
        else:
            msg += f"B : {move_coords}\n"
            session['A_turn'] = True
        data['content'] = msg
        data['is_started'] = True

        dynamic_URL = static_URL + new_position
        session['moves_data'] = requests.get(url=dynamic_URL).json()['moves']
        session['starting_position'] = new_position

    return render_template('handle.html', post=data)
