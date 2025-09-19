from app import create_app

app = create_app() 

import sys
print(f"--- Running with Python from: {sys.executable} ---")


if __name__ == ('__main__'):
  app.run(debug=True)
  