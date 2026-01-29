Python Project Setup
This guide will help you set up your local development environment.

1. Activate the Virtual Environment
Before installing packages or running scripts, you must activate the virtual environment (venv). This ensures your project uses a localized Python interpreter.

```bash
    venv\Scripts\activate
```

or

```bash
    .\venv\Scripts\Activate.ps1
```

2. Install Dependencies
Once the environment is active, use the Python Package Index (pip) to install the required libraries from the requirements.txt file.

```bash
pip install -r requirements.txt
```

3. Run Environment Check
To verify that everything is installed correctly and your environment is configured as expected, run the env_check script.

```bash
python env_check.py
```