import os

# Database configuration
PGHOST = os.environ.get('PGHOST')
PGPORT = os.environ.get('PGPORT')
PGDATABASE = os.environ.get('PGDATABASE')
PGUSER = os.environ.get('PGUSER')
PGPASSWORD = os.environ.get('PGPASSWORD')
DATABASE_URL = os.environ.get('DATABASE_URL')

# Application secret key
SECRET_KEY = os.urandom(24)

# Groq API configuration
GROQ_API_KEY = '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'  # Replace with actual API key
GROQ_API_URL = 'https://api.groq.com/v1/completions'
