# dash-app-structure

 The software architecture design is inspired by [this repository.](https://github.com/bradley-erickson/dash-app-structure).

## Install and Setup

To get started with the app, follow these steps for installation and setup:

1. **Clone the Repository**  
Clone the project to your local machine and navigate to the directory where the project was cloned:
   ```bash
   git clone https://github.com/amirjaf/equity_dash.git
   cd equity_dash
   ```

2. **Data Request**  
Request the necessary data and place it in the `src/assets/data` directory. If the `data` folder does not exist, create it first:
   ```bash
   mkdir -p src/assets/data
   ```

3. **Install the Virtual Environment and Requirements**  
Make sure your system has Python installed and the functionality to create a virtual environment.

```bash
python -m venv .venv                            # Create a virtual environment in the current directory
.venv\Scripts\pip install -r requirements.txt   # Install the required dependencies
```

4. **Run the Dashboard Application**  
Run the Dash app from the current directory:

```bash
.venv\Scripts\python src\app.py                 # Run the application
```

## Structure

This repository serves as a guide for structuring large Dash applications.
The ideas presented in this guide come from my own experience working in large React projects and common attributes found in open source repositories.

The following is an overview of the structure.
I will follow the structure from top down, covering each item and its purpose.
Additionally, I've created this repository to demonstrate the structure and serve as a template for anyone who wants to fork it.
Each file in the repository includes more information about the purpose of the file.

```bash
dash-app-structure
|-- .venv
|   |-- *
|-- .gitattributes
|-- .gitignore
|-- Dockerfile
|-- License
|-- Procfile
|-- README.md
|-- requirements.txt
|-- src
|   |-- assets
|   |   |-- logos/
|   |   |-- css/
|   |   |-- images/
|   |   |-- favicon.ico
|   |-- components
|   |   |-- __init__.py
|   |   |-- footer.py
|   |   |-- navbar.py
|   |   |-- navbar_vertical.py
|   |   |-- line_chart_AIO.py
|   |   |-- pie_chart_AIO.py
|   |-- pages
|   |   |-- __init__.py
|   |   |-- tour_page
|   |   |   |-- __init__.py
|   |   |   |-- hispanic.py
|   |   |   |-- income.py
|   |   |   |-- load_tour_data.py
|   |   |   |-- main.py
|   |   |   |-- race.py
|   |   |-- home.py
|   |   |-- not_found_404.py
|   |-- utils
|   |   |-- __init__.py
|   |   |-- api.py
|   |   |-- data_handling.py
|   |   |-- data_loader.py
|   |   |-- images.py
|   |   |-- settings.py
|   |-- app.py
|   |-- cache.py
|   |-- gunicorn_config.py
|   |-- server.py
|-- tests
|   |-- *

```

### Virtual Environment

The first few items in our structure refer to the virtaul environment and package manager.
This is a must for handling large applications and ensuring that packages are using the correct versions.

The `.venv` directory is the virtual environment itself where the project specific Python package versions are located.
There are various ways to create this, but use the first command below.
Note that `.venv` is a common name to use for your virtual environment.
The `requirements.txt` file contains the required Python packages and their respective versions for running the application.
I've included some additional commands for installing the current requirements, adding new packages, and updating the requirments file.

```bash
python -m venv .venv                            # create the virtual environment
.venv\Scripts\pip install -r requirements.txt   # install all packages
.venv\Scripts\pip install new_package           # install a new package
.venv\Scripts\pip freeze > requirements.txt     # update requirements with new packages
```

Note: there is a small shift in the Python community away from using `venv` and instead using `pipenv`.
At the time of writing this, I am not as familiar with `pipenv` as and I am with using `venv`.

### Environment Variables

The `.env.development` file is where you should store sensitive information such as passwords or API keys.  
This is a common practice to avoid hardcoding keys directly into your application, which could expose them to potential security risks.  
Some common values found in `.env.development` files include `DATABASE_URI` or `API_KEY`.

You can also substitute this file with another `.env` file, such as `.env.production`, when running the app in different environments (e.g., development vs. production). To do this, set the `ENVIRONMENT_FILE` environment variable to point to the desired `.env` file. For example:
```bash
export ENVIRONMENT_FILE=.env.production
```






