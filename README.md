# Manchester Storm Dashboard

This repository contains a web-based dashboard for Manchester Storm, a hockey team, which includes a public-facing dashboard and an admin panel for real-time game management.

## Overview

- **app.py**: The main backend script for the Manchester Storm dashboard application. It uses Flask to handle HTTP requests, manage game state, and render the appropriate templates for the dashboard and admin panel.
- **dashboard.html**: The front-end template for displaying the game status, including scores, events, and the current stage of the game.
- **admin.html**: The front-end template for the admin panel where administrators can update game details and handle messages.
- **events.html**: The front-end template for the events management page.
- **rundown.html**: The front-end template for the rundown
- **edit_rundown.html**: Front end template for manaing the rundown
- **import_rundown.html**: Front end template for importing JSON rundowns
- **control.html**: vMix Remote Control Interface
- **buttonedit.html**: Allows management of buttons on the vMix Remote Control Interface

## Files

### app.py

This is the core Python script for the application. It utilizes Flask to create a web server that serves the dashboard and admin panel.

**Functions:**
- **get_vmix_data():**
    - Purpose: Fetches live data from the vMix API.
    - Behavior: Sends a GET request to the vMix API endpoint. If the request is successful, the response data (XML) is returned. If there’s a connection error or timeout, it returns None and prints an error message.

- **get_vmix_data_cached():**
    - Purpose: Retrieves vMix data with caching to reduce the number of API calls.
    - Behavior: Checks if cached data is available and not older than 10 seconds. If valid cached data is available, it returns the cached data. Otherwise, it fetches fresh data using get_vmix_data(), caches it, and then returns it.

- **get_score_from_title(xml_data):**
    - Purpose: Extracts team scores from the XML data provided by the vMix API.
    - Behavior: Parses the XML data to locate the Scoreboard title and extracts the scores for two teams. Returns the scores as a tuple. If parsing fails, it returns (0, 0).

**Routes:**
- **/ (dashboard):**

     - Purpose: Displays the main dashboard.
      - Behavior: Fetches vMix data (cached) and updates the team scores in the app state. Renders the dashboard.html template with the current rundown and state.

- **/data:**
    - Purpose: Provides the current app state as JSON.
    - Behavior: Fetches vMix data (cached) and updates the team scores. Returns the updated app state as a JSON response.

- **/admin:**
    - Purpose: Admin panel for managing the app's state.
    - Behavior: Handles login and updates to the current stage, teams, and messages. Renders the admin.html template with the current state. Supports POST requests for updating the state and login.

**/roster:**
    - Purpose: Displays the team rosters.
    - Behavior: Renders the roster.html template with the available teams and current app state.

**/get_roster:**
    - Purpose: Fetches the roster for a specific team.
    - Behavior: Accepts a POST request with the team name and returns the roster data for that team as JSON.

- **/events:**
    - Purpose: Manages events and requires authentication.
    
    - Behavior: Handles login for the events section and allows adding and editing events if the user is authenticated. Renders the events.html template.

- **/rundown:**
    - Purpose: Displays the rundown of events.
    Behavior: Renders the rundown.html template with the current rundown and app state.

- **/edit_rundown:**
    - Purpose: Allows editing of the rundown.
    Behavior: Handles POST requests to add a new segment to the rundown. Renders the edit_rundown.html template for editing the rundown.

- **/export_rundown:**
    - Purpose: Exports the current rundown as a JSON file.
    - Behavior: Serializes the rundown to JSON and returns it as a downloadable file.

- **/import_rundown:**
    - Purpose: Allows importing a rundown from a JSON file.
    - Behavior: Handles file uploads and imports the rundown, updating the app's state. Renders the import_rundown.html template.

- **/reorder_rundown:**
    - Purpose: Reorders the rundown segments.
    - Behavior: Accepts a POST request with the new order of segments and updates the rundown accordingly. Returns a JSON response indicating success.

- **/edit_rundown_segment/<int:segment_number>:**
    - Purpose: Edits a specific rundown segment.
    Behavior: Updates a segment based on the provided segment number and data. Returns a JSON response indicating success.

 - **/delete_rundown_segment/<int:segment_number>:**
    - Purpose: Deletes a specific rundown segment.
    Behavior: Removes the specified segment from the rundown and reorders the remaining segments. Returns a JSON response indicating success.

- **/set_current_segment/<int:segment_number>:**
    - Purpose: Sets the current segment in the rundown.
    Behavior: Updates the app state with the specified segment number as the current segment. Returns a JSON response indicating success.

- **/vmix_control:**
    - Purpose: Displays the vMix control panel.
    Behavior: Retrieves the list of buttons from the database and renders the control.html template with these buttons and the current app state.

- **/edit_vmix_buttons:**
    - Purpose: Provides an interface to edit vMix control buttons.
    Behavior: Retrieves the list of buttons from the database and renders the buttonedit.html template for editing buttons.

- **/api/vmix_control:**
    - Purpose: API endpoint to trigger vMix commands based on button actions.
    - Behavior: Handles POST requests to execute vMix functions like changing the program, playing/pausing, restarting an input, or selecting a playlist. Returns a JSON response indicating success or failure.

- **/api/edit_vmix_buttons:**
    - Purpose: API endpoint to add or update vMix control buttons.
    - Behavior: Handles POST requests to create or update a button in the database. Redirects to the edit_vmix_buttons page with a status indicating success or failure.

- **/api/delete_vmix_button:**
    - Purpose: API endpoint to delete a vMix control button.
    - Behavior: Handles POST requests to delete a button from the database. Redirects to the edit_vmix_buttons page with a status indicating success or failure.

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

### admin.html

The `admin.html` file provides the interface for administrators to manage the game state and send messages.

**Key Features:**
- **Game Management:**
  - Allows updating the current stage, home team, and away team.
  - Provides a textarea to input or clear a message.
- **Authentication:**
  - Provides a login form for admin access.

### events.html
The `events.html` file provides the interface for administrators to manage events.

**Key Features:**
- **Event Management**
  - Form to add new events with timesands.
  - Editable lis of existing evens with options to edit.
- **Authentication:**
  - Provides a login form for access.

### control.html
The `control.html` file provides the interface for vMix Remote Control


### buttonedit.html
The `buttonedit.html` file provides the interface for editing buttons on the vMix Remote Control

### rundown.html
The `rundown.html` file provides the interface for viewing the broadcast rundown

### edit_rundown.html
The `edit_rundown.html` file provides the interface for editing the broadcast rundown

### roster.html
The `roster.html` file provides the interface for viewing team rosters

### import_rundown.html
The `import_rundown.html` file provides the interface for importing JSON rundowns

### vmix_buttons.db
SQLite database to store the vMix Control Buttons

### roster_data.json
JSON file containing team roster data

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
git clone https://github.com/TrixR6/manchester_storm_dashboard.git
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

When accessing the events panel at [http://127.0.0.1:5000/events](http://127.0.0.1:5000/admin), use the following default credentials:

- **Username:** `events_admin`
- **Password:** `events_password`

