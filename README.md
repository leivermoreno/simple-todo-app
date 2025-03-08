# TODO Flask App

This is a simple TODO application built with Flask. It allows users to create projects, add tasks, and collaborate with other users.

## Main features

- User registration and authentication
- Create, update, and delete projects
- Add, update, and delete tasks within projects
- Invite collaborators to projects. Collaborators can be removed later
- Mark tasks as completed or uncompleted

## Usage

- Email: `testuser1@mailservice.com`
- Password: `pass`

## Setup

### Installation

1. Clone the repository and change directory into it:

    ```sh
    git clone https://github.com/leivermoreno/simple-todo-app.git
    cd todo_flask_app
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

### Running the Application
1. Run the Flask development server:

    ```sh
    flask --app todo_app/app.py run
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`