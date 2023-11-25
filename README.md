# Zionnet API

## Installation Instructions

### Prerequisites

Before setting up the project locally, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/downloads/) (>=3.11.4)
- A Database System (e.g., PostgreSQL, MySQL, SQLite) - [Django Database Installation](https://www.djangoproject.com/download/#database-installation)

### Installation Steps

1. Clone the repository:

        git clone https://github.com/zionet-app/zionnet_backend.git


2. Change into the parent directory:

        cd zionnet_backend


3. Set up a virtual environment:

        pipenv install


4. Activate your virtual environment:

        pipenv shell


5. Install the Python dependencies:

        pipenv install -r requirements.txt


6. Create a .env file and set necessary secret keys.


7. Apply migrations to create the database schema:

        python3 manage.py migrate


8. Start the development server: 
 ```
 python3 manage.py runserver
 ```

The API should now be running locally at [http://localhost:8000/](http://localhost:8000/).


# Commit Standards

## Branches

- **dev** -> pr this branch for everything `backend` related
- **Master** -> **don't touch** this branch!

## Contribution Guidelines

1. Clone the repo `git clone https://github.com/zionet-app/zionnet_backend.git`.
2. Open your terminal & set the origin branch: `git remote add origin https://github.com/zionet-app/zionnet_backend.git`
3. Pull origin `git pull origin dev`
4. Create a new branch for the task you were assigned to, eg `Zionnet_project_part/(Feat/Bug/Fix/Chore)/specific feature` : `git checkout -b Authentication/Feat/Sign-Up-from`
5. After making changes, do `git add .`
6. Commit your changes with a descriptive commit message : `git commit -m "your commit message"`.
7. To make sure there are no conflicts, run `git pull origin dev`.
8. Push changes to your new branch, run `git push -u origin Authentication/Feat/Sign-Up-from`.
9. Create a pull request to the `dev` branch not `Master`.
10. Ensure to describe your pull request.
11. > If you've added code that should be tested, add some test examples.

### _Commit CheatSheet_

| Type     |                          | Description                                                                                                 |
| -------- | ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| feat     | Features                 | A new feature                                                                                               |
| fix      | Bug Fixes                | A bug fix                                                                                                   |
| docs     | Documentation            | Documentation only changes                                                                                  |
| style    | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)      |
| refactor | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                                   |
| perf     | Performance Improvements | A code change that improves performance                                                                     |
| test     | Tests                    | Adding missing tests or correcting existing tests                                                           |
| build    | Builds                   | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
| ci       | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
| chore    | Chores                   | Other changes that don't modify, backend or test files                                                    |
| revert   | Reverts                  | Reverts a previous commit                                                                                   |

> _Sample Commit Messages_

- `chore: Updated README file`:= `chore` is used because the commit didn't make any changes to the frontend or test folders in any way.
- `feat: Added plugin info endpoints`:= `feat` is used here because the feature was non-existent before the commit.
