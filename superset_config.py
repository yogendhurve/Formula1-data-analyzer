# superset_config.py

# 1. Your generated secret key (REQUIRED)
SECRET_KEY = 'YOUR_GENERATED_SECRET_KEY_GOES_HERE' 

# 2. PostgreSQL Metadata Database URI (REQUIRED)
# Password 'Jarvis@890' is encoded as 'Jarvis%40890'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Jarvis%40890@localhost:5432/f1_analytics'