# Zionnet API

## Prerequisites

Before setting up the project locally, ensure you have the following prerequisites installed:

- A [Python](https://www.python.org/downloads/) Installation (>=3.11.4)
- A Database Management System (e.g., PostgreSQL, MySQL, SQLite) - [Django Database Installation](https://www.djangoproject.com/download/#database-installation)

## Installation

Here are the steps to getting this API up and running:

1.  Open your favourite terminal and navigate to a suitable directory.  

    ```bash
    cd path/to/suitable/directory/
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/zionet-app/zionnet_backend
    ```

3. Navigate to the root directory
    ```bash
    cd zionnet_backend
    ```

4. Set up a virtual environment  
    - Windows

        ```bash
        python -m virtualenv venv
        venv\Scripts\activate
        ```
    - Mac / Linux

        ```bash
        python3 -m virtualenv venv
        source venv/bin/activate
        ```

5. Install the project's dependencies
    - Windows

        ```bash
        python -m pip install -r requirements.txt
        ```
    - Mac / Linux

        ```bash
        python3 -m pip3 install -r requirements.txt
        ```

6. Run a Local Development server on port 8000 (or any suitable port of your choice)
    - Windows

        ```bash
        python manage.py runserver
        ```
    - Mac / Linux

        ```bash
        python3 manage.py runserver
        ```

7. That's it 🎉. Start interacting with the endpoints locally.

    Alternatively, if you have a local server running on port 8000,
    - You could use the swagger documentation (probably [here](http://localhost:8000/api/v1/swagger/) or at `/api/v1/swagger/` ).
    - You could use the redoc documentation (probably [here](http://localhost:8000/api/v1/redoc/) or at `/api/v1/redoc/` ).
    - You could also visit the endpoints URLs in the browsable API if you'd like.


## Commit Standards

### Branches

- **dev** => Make all Pull requests towards this branch
- **Master** => **Don't touch** this branch!

### Contribution Guidelines

1. Clone the repository `git clone https://github.com/zionet-app/zionnet_backend.git`.
2. Open your terminal & set the origin branch: `git remote add origin https://github.com/zionet-app/zionnet_backend.git`
3. Pull from the `dev` branch: `git pull origin dev`
4. Create a new branch for the task you were assigned to, eg `Zionnet_project_part/(Feat/Bug/Fix/Chore)/specific feature` => `git checkout -b Authentication/Feat/Sign-Up-form`
5. After making changes, do `git add .`
6. Commit your changes with a descriptive commit message : `git commit -m "your commit message"`.
7. To make sure there are no conflicts, run `git pull origin dev`.
8. Push changes to your new branch, run `git push -u origin Authentication/Feat/Sign-Up-form`.
9. Create a pull request towards the `dev` branch not `Master`.
10. Ensure to describe your pull request.
11. > If you've added code that should be tested, add some test examples.

### _Commit CheatSheet_

| Type     |                          | Description                                                                                                 
| -------- | ------------------------ | -----------------------------------------------------------------------------------------------------------
| feat     | Features                 | A new feature
| fix      | Bug Fixes                | A bug fix
| docs     | Documentation            | Documentation only changes
| style    | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)
| refactor | Code Refactoring         | A code change that neither fixes a bug nor adds a feature
| perf     | Performance Improvements | A code change that improves erformance
| test     | Tests                    | Adding missing tests or correcting existing tests
| build    | Builds                   | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
| ci       | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
| chore    | Chores                   | Other changes that don't modify, backend or test files
| revert   | Reverts                  | Reverts a previous commit

#### _Sample Commit Messages_

- _chore: Updated README file_ : `chore` is used because the commit didn't make any changes to the frontend or test folders in any way.
- _feat: Added plugin info endpoints_ : `feat` is used here because the feature was non-existent before the commit.
- _ci: Added a 'Run Migrations' step to the workflow_ : `ci` is used because the commit makes changes to one of the CI/CD files.
