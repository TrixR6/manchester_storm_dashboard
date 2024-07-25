# Manchester Storm Dashboard

This repository contains a web-based dashboard for Manchester Storm, a hockey team, which includes a public-facing dashboard and an admin panel for real-time game management.

## Overview

- **app.py**: The main backend script for the Manchester Storm dashboard application. It uses Flask to handle HTTP requests, manage game state, and render the appropriate templates for the dashboard and admin panel.
- **dashboard.html**: The front-end template for displaying the game status, including scores, events, and the current stage of the game.
- **admin.html**: The front-end template for the admin panel where administrators can update game details, manage events, and handle messages.

## Files

### app.py

This is the core Python script for the application. It utilizes Flask to create a web server that serves the dashboard and admin panel.

**Key Features:**
- **Routes:**
  - `/`: Displays the public dashboard showing the current game status.
  - `/admin`: Displays the admin panel for managing game details and events.
  - `/data`: Provides a JSON API endpoint for the dashboard to fetch real-time game data.
- **Templates:**
  - Renders `dashboard.html` and `admin.html` based on the route requested.
- **State Management:**
  - Maintains game state including team scores, current stage, and events.
- **Authentication:**
  - Simple authentication check for accessing the admin panel.

**Example Usage:**
To run the application, use:

```bash
python app.py
```
### dashboard.html

The `dashboard.html` file is the public-facing template that displays real-time information about the ongoing game.

**Key Features:**
- **Navbar:**
  - Provides links to the dashboard, admin panel, and relevant external sites.
- **Game Status:**
  - Shows home and away team names and logos.
  - Displays current scores and game stage.
- **Events Timeline:**
  - Lists events occurring in the game with timestamps.
- **Dynamic Updates:**
  - Uses JavaScript to periodically fetch new game data and update the page.

**Key HTML Elements:**
- `<nav>`: Contains the navigation bar.
- `<div id="messageBox">`: Displays messages if sent.
- `<div id="gameTitle">`: Shows game title and team scores.
- `<div class="events-timeline">`: Lists events in the game.

### admin.html

The `admin.html` file provides the interface for administrators to manage the game state and send messages.

**Key Features:**
- **Game Management:**
  - Allows updating the current stage, home team, and away team.
  - Provides a textarea to input or clear a message.
- **Authentication:**
  - Provides a login form for admin access.

### admin.html
The `events.html` file provides the interface for administrators to manage events.

**Key Features:**
- **Event Management**
  - Form to add new events with timesands.
  - Editable lis of existing evens with options to edit.
- **Authentication:**
  - Provides a login form for access.


### vMix API Integration

The application pulls the latest game scores from the vMix API using the following code block in `app.py`
```python
for title in titles:
    if title.get('title') == "Scoreboard":  # Replace with your actual title name
        team1_score_element = title.find(".//text[@name='Team1Score.Text']")
        team2_score_element = title.find(".//text[@name='Team2Score.Text']")
        if team1_score_element is not None and team2_score_element is not None:
            team1_score = team1_score_element.text
            team2_score = team2_score_element.text
            return int(team1_score), int(team2_score)
```

If you are using text holders other than `Team1Score.Text` or `Team2Score.Text` please be ensure to updae this here.
```python
        team1_score_element = title.find(".//text[@name='Team1Score.Text']")
        team2_score_element = title.find(".//text[@name='Team2Score.Text']")
```
If your tital in your vMix package is not `"Scoreboard"` please also update this here 
```python
if title.get('title') == "Scoreboard":
```
## Setup

**Clone the Repository:**

```bash
git clone https://github.com/yourusername/manchester_storm_dashboard.git
```

**Install Dependancies:**

Ensure you have Flask installed. If not, you can install it using pip:
```bash
pip install flask
```

**Run the application:**
```bash
python app.py
```

**Access the Dashboard:**
Open your web browser and navigate to http://127.0.0.1:5000/. Alternatively, this can be accessed from your computers IP and port e.g. http://192.168.0.10:5000/

**Access the Admin Panel:**
Navigate to http://127.0.0.1:5000/admin. You'll need to log in to make changes. Alternatively, this can be accessed from your computers IP and port e.g. http://192.168.0.10:5000/admin

## Default Credentials

When accessing the admin panel at [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin), use the following default credentials:

- **Username:** `admin`
- **Password:** `password`

