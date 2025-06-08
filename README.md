# Streamlit Application

This is a template for a Streamlit application with a well-organized project structure.

## Project Structure
```
.
├── src/            # Source code files
│   └── app.py      # Main Streamlit application
├── data/           # Data files
├── config/         # Configuration files
├── assets/         # Static files (images, etc.)
├── tests/          # Unit tests
└── requirements.txt # Python dependencies
```

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the Streamlit app:
```bash
streamlit run src/app.py
```

The application will open in your default web browser at http://localhost:8501. 