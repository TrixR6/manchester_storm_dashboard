from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file, make_response
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import json
import io
import os

app = Flask(__name__)
app.secret_key = 'BingBong'
rundown = []

app_state = {
    'is_logged_in': False,
    'current_stage': 'Pre Show',
    'game_title': 'Manchester Storm vs Sheffield Steelers',
    'home_team': 'Manchester Storm',
    'home_team_logo': 'https://www.eliteleague.co.uk/photo/team/team_11.png',
    'away_team': 'Sheffield Steelers',
    'away_team_logo': 'https://www.eliteleague.co.uk/photo/team/team_13.png',
    'message': '',
    'is_message_sent': False,
    'team1_score': 0,
    'team2_score': 0,
    'events': [],
    'current_segment': None
}

teams = {
    'Manchester Storm': 'https://www.eliteleague.co.uk/photo/team/team_11.png',
    'Belfast Giants': 'https://www.eliteleague.co.uk/photo/team/team_4.png',
    'Cardiff Devils': 'https://www.eliteleague.co.uk/photo/team/team_5.png',
    'Coventry Blaze': 'https://www.eliteleague.co.uk/photo/team/team_6.png',
    'Dundee Stars': 'https://www.eliteleague.co.uk/photo/team/team_7.png',
    'Fife Flyers': 'https://www.eliteleague.co.uk/photo/team/team_8.png',
    'Glasgow Clan': 'https://www.eliteleague.co.uk/photo/team/team_9.png',
    'Guildford Flames': 'https://www.eliteleague.co.uk/photo/team/team_10.png',
    'Nottingham Panthers': 'https://www.eliteleague.co.uk/photo/team/team_12.png',
    'Sheffield Steelers': 'https://www.eliteleague.co.uk/photo/team/team_13.png',
    'Université du Québec à Trois-Rivières Patriotes': 'https://upload.wikimedia.org/wikipedia/en/c/ca/UQTR_Patriotes_Logo.png',
    'Lausitzer Füchse': 'https://upload.wikimedia.org/wikipedia/en/5/57/Logo_Lausitzer_F%C3%BCchse.png'
}

vmix_cache = {
    'data': None,
    'timestamp': 0
}

def get_vmix_data():
    try:
        response = requests.get("http://localhost:8088/api", timeout=2)
        if response.status_code == 200:
            return response.text
        return None
    except requests.ConnectionError:
        print("Error: Unable to connect to vMix API")
        return None
    except requests.Timeout:
        print("Error: Connection to vMix API timed out")
        return None

def get_vmix_data_cached():
    current_time = time.time()
    if vmix_cache['data'] is None or (current_time - vmix_cache['timestamp']) > 10:  # Cache for 10 seconds
        vmix_cache['data'] = get_vmix_data()
        vmix_cache['timestamp'] = current_time
    return vmix_cache['data']

def get_score_from_title(xml_data):
    if not xml_data:
        return 0, 0

    try:
        root = ET.fromstring(xml_data)
        titles = root.findall(".//input")
        for title in titles:
            if title.get('title') == "Scoreboard":
                team1_score_element = title.find(".//text[@name='Team1Score.Text']")
                team2_score_element = title.find(".//text[@name='Team2Score.Text']")
                if team1_score_element is not None and team2_score_element is not None:
                    team1_score = team1_score_element.text
                    team2_score = team2_score_element.text
                    return int(team1_score), int(team2_score)
    except ET.ParseError:
        print("Error: Failed to parse XML data")
    
    return 0, 0

@app.route('/')
def dashboard():
    data = get_vmix_data_cached()
    if data:
        team1_score, team2_score = get_score_from_title(data)
        app_state['team1_score'] = team1_score
        app_state['team2_score'] = team2_score
    now = datetime.now()
    return render_template('dashboard.html', rundown=rundown, state=app_state, now=now)

@app.route('/data')
def data():
    data = get_vmix_data_cached()
    if data:
        team1_score, team2_score = get_score_from_title(data)
        app_state['team1_score'] = team1_score
        app_state['team2_score'] = team2_score
    return jsonify(app_state)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            if username == 'admin' and password == 'password':
                app_state['is_logged_in'] = True
            return redirect(url_for('admin'))
        
        if 'update' in request.form:
            app_state['current_stage'] = request.form['stage']
            app_state['home_team'] = request.form['home_team']
            app_state['home_team_logo'] = teams[request.form['home_team']]
            app_state['away_team'] = request.form['away_team']
            app_state['away_team_logo'] = teams[request.form['away_team']]
            app_state['message'] = request.form['message']
            app_state['is_message_sent'] = True if request.form['message'] else False
            return redirect(url_for('admin'))
        
        if 'clear' in request.form:
            app_state['message'] = ''
            app_state['is_message_sent'] = False
            return redirect(url_for('admin'))
    
    return render_template('admin.html', state=app_state)

with open('roster_data.json') as f:
    roster_data = json.load(f)

@app.route('/roster')
def roster():
    teams = roster_data.keys()
    return render_template('roster.html', teams=teams, state=app_state)

@app.route('/get_roster', methods=['POST'])
def get_roster():
    team = request.json['team']
    if team in roster_data:
        return jsonify(roster_data[team])
    else:
        return jsonify([])

@app.route('/events', methods=['GET', 'POST'])
def events():
    if 'events_logged_in' not in session:
        if request.method == 'POST' and 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            if username == 'events_admin' and password == 'events_password':  # Change credentials
                session['events_logged_in'] = True
                return redirect(url_for('events'))
        return render_template('events.html', state={'login_required': True})

    if request.method == 'POST':
        if 'add_event' in request.form:
            new_event = request.form.get('new_event')
            timestamp = request.form.get('timestamp')
            if new_event and timestamp:
                app_state['events'].insert(0, {'timestamp': timestamp, 'content': new_event})
            return redirect(url_for('events'))
        
        if 'edit_event' in request.form:
            event_index = int(request.form['edit_event'])
            app_state['events'][event_index]['content'] = request.form['event_content']
            app_state['events'][event_index]['timestamp'] = request.form['event_timestamp']
            return redirect(url_for('events'))
    
    return render_template('events.html', state=app_state)

@app.route('/rundown')
def show_rundown():
    return render_template('rundown.html', rundown=rundown, state=app_state)

@app.route('/edit_rundown', methods=['GET', 'POST'])
def edit_rundown():
    if request.method == 'POST':
        segment_number = len(rundown) + 1
        new_segment = {
            'number': segment_number,
            'item_name': request.form['item_name'],
            'start_time': request.form['start_time'],
            'duration': request.form['duration'],
            'notes': request.form['notes'],
            'video': request.form['video'],
            'graphics': request.form['graphics'],
            'audio': request.form['audio'],
            'script': request.form['script'],
            'talent': request.form['talent'],
            'color': request.form['color'].lower(),
            'color_name': request.form['color']
        }

        if new_segment['color'] == 'purple':
            new_segment['color'] = '#D8BFD8'  # Light purple
        rundown.append(new_segment)
        save_rundown_state()
        return redirect(url_for('show_rundown'))
    return render_template('edit_rundown.html', state=app_state)

@app.route('/export_rundown')
def export_rundown():
    json_rundown = json.dumps(rundown, indent=4)
    buffer = io.StringIO()
    buffer.write(json_rundown)
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=rundown.json'
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/import_rundown', methods=['GET', 'POST'])
def import_rundown():
    if request.method == 'POST':
        file = request.files['json_file']
        if file:
            imported_rundown = json.load(file)
            global rundown
            rundown = imported_rundown
            save_rundown_state()
            return redirect(url_for('show_rundown'))
    return render_template('import_rundown.html', state=app_state)

@app.route('/reorder_rundown', methods=['POST'])
def reorder_rundown():
    new_order = request.json['new_order']
    global rundown
    reordered_rundown = [None] * len(rundown)
    
    for i, segment_number in enumerate(new_order):
        for segment in rundown:
            if segment['number'] == segment_number:
                reordered_rundown[i] = segment
                break
    
    for i, segment in enumerate(reordered_rundown):
        segment['number'] = i + 1
    
    rundown = reordered_rundown
    save_rundown_state()
    return jsonify({"status": "success"})

@app.route('/edit_rundown_segment/<int:segment_number>', methods=['POST'])
def edit_rundown_segment(segment_number):
    updated_segment = request.json
    global rundown

    for segment in rundown:
        if segment['number'] == segment_number:
            segment.update(updated_segment)
            break
    
    save_rundown_state()
    return jsonify({"status": "success"})

@app.route('/delete_rundown_segment/<int:segment_number>', methods=['POST'])
def delete_rundown_segment(segment_number):
    global rundown
    rundown = [segment for segment in rundown if segment['number'] != segment_number]

    for i, segment in enumerate(rundown):
        segment['number'] = i + 1

    save_rundown_state()
    return jsonify({"status": "success"})

@app.route('/set_current_segment/<int:segment_number>', methods=['POST'])
def set_current_segment(segment_number):
    global app_state
    app_state['current_segment'] = segment_number
    save_rundown_state()
    return jsonify({"status": "success"})

def save_rundown_state():
    with open('rundown_state.json', 'w') as f:
        json.dump({'rundown': rundown, 'state': app_state}, f)

def load_rundown_state():
    global rundown, app_state
    if os.path.exists('rundown_state.json'):
        with open('rundown_state.json', 'r') as f:
            data = json.load(f)
            rundown = data.get('rundown', [])
            app_state = data.get('state', app_state)

load_rundown_state()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
