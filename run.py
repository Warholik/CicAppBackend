import os
from dotenv import load_dotenv, find_dotenv

from app import create_app

load_dotenv(find_dotenv())

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

if __name__ == '__main__':
  port = os.getenv('PORT')
  # run app
  print(f"env:  {env_name}")
  print(f"port:  {port}")
  app.run(host='127.0.0.1', port=5000)