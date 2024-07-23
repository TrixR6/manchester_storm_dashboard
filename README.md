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

The `admin.html` file provides the interface for administrators to manage the game state and events.

**Key Features:**
- **Game Management:**
  - Allows updating the current stage, home team, and away team.
  - Provides a textarea to input or clear a message.
- **Event Management:**
  - Form to add new events with timestamps.
  - Editable list of existing events with options to edit.
- **Authentication:**
  - Provides a login form for admin access.

**Key HTML Elements:**
- `<form method="POST">`: Used for updating game state and events.
- `<textarea>`: For inputting messages and event content.
- `<select>`: For choosing game stages and teams.
- `<button>`: For submitting forms and interacting with the admin panel.

### /data Endpoint

The `/data` endpoint provides a JSON API for the public dashboard to fetch real-time game data.

**Key Features:**
- **Data Provided:**
  - The endpoint returns a JSON object containing:
    - `current_stage`: The current stage of the game (e.g., "1st Period").
    - `home_team`: The name of the home team.
    - `away_team`: The name of the away team.
    - `home_score`: The current score of the home team.
    - `away_score`: The current score of the away team.
    - `events`: A list of events occurring in the game, each with a timestamp and content.

**Example Response:**

```json
{
  "current_stage": "1st Period",
  "home_team": "Manchester Storm",
  "away_team": "Belfast Giants",
  "home_score": 2,
  "away_score": 1,
  "events": [
    {
      "timestamp": "10:15",
      "content": "Manchester Storm goal by Player X"
    },
    {
      "timestamp": "15:42",
      "content": "Belfast Giants goal by Player Y"
    }
  ]
}
```
**Usage:**
- The dashboard uses this endpoint to periodically request updates and refresh the displayed game data without needing a full page reload.

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

