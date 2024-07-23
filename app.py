from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

app_state = {
    'is_logged_in': False,
    'current_stage': 'Pre Show',
    'game_title': 'Manchester Storm vs Opponent',
    'home_team': 'Manchester Storm',
    'home_team_logo': 'https://www.eliteleague.co.uk/photo/team/team_11.png',
    'away_team': 'Opponent',
    'away_team_logo': '',
    'message': '',
    'is_message_sent': False,
    'team1_score': 0,
    'team2_score': 0,
    'events': []
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
    'Sheffield Steelers': 'https://www.eliteleague.co.uk/photo/team/team_13.png'
}

def get_vmix_data():
    try:
        response = requests.get("http://localhost:8088/api")
        if response.status_code == 200:
            return response.text
        return None
    except requests.ConnectionError:
        print("Error: Unable to connect to vMix API")
        return None

def get_score_from_title(xml_data):
    if not xml_data:
        return 0, 0

    root = ET.fromstring(xml_data)
    titles = root.findall(".//input")

    for title in titles:
        if title.get('title') == "Scoreboard":  # Replace with your actual title name
            team1_score_element = title.find(".//text[@name='Team1Score.Text']")
            team2_score_element = title.find(".//text[@name='Team2Score.Text']")
            if team1_score_element is not None and team2_score_element is not None:
                team1_score = team1_score_element.text
                team2_score = team2_score_element.text
                return int(team1_score), int(team2_score)
    
    return 0, 0

@app.route('/')
def dashboard():
    data = get_vmix_data()
    if data:
        team1_score, team2_score = get_score_from_title(data)
        app_state['team1_score'] = team1_score
        app_state['team2_score'] = team2_score
    now = datetime.now()
    return render_template('dashboard.html', state=app_state, now=now)

@app.route('/data')
def data():
    data = get_vmix_data()
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
            new_event = request.form.get('new_event')
            timestamp = request.form.get('timestamp')
            if new_event and timestamp:
                app_state['events'].insert(0, {'timestamp': timestamp, 'content': new_event})
            return redirect(url_for('admin'))
        
        if 'clear' in request.form:
            app_state['message'] = ''
            app_state['is_message_sent'] = False
            return redirect(url_for('admin'))
        
        if 'edit_event' in request.form:
            event_index = int(request.form['edit_event'])
            app_state['events'][event_index]['content'] = request.form['event_content']
            app_state['events'][event_index]['timestamp'] = request.form['event_timestamp']
            return redirect(url_for('admin'))
    
    return render_template('admin.html', state=app_state)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
