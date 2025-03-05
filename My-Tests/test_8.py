"""
So you want to use the Postgres Array Comparator.

# query = session.query(TestUser).filter(TestUser.numbers.contains([some_int])).all()
or

# query = session.query(TestUser).filter(TestUser.numbers.any(25)).all()
"""

"""
from dotenv import load_dotenv
load_dotenv()

Now all your key=value pairs will be loaded into your application. You can use the variable as,
import os
SECRET_KEY = os.getenv("MY_SECRET")

Create your .env file along-side your settings/config file.
.
├── .env
└── config.py
"""
from dotenv import load_dotenv;
load_dotenv();

import os;
MY_SECRET = os.getenv('MY_SECRET');
print(MY_SECRET);

APP_NAME = os.getenv('APP_NAME');
print(APP_NAME);