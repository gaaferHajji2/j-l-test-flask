# stores={};
# items={};

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# After install the flask-migrate, we run the command:
# flask db init.

# After that we run : flask db migrate
# And this will generate the data of our db.

# Then we create the db using command: flask db upgrade

# When we change models, like adding new cols, data, ...etc.
# we can reflect the changes using: 
# flask db migrate && flask db upgrade.

# to execute a raw sql query from alembic migration;
# we can use op.execute("Query Here LIKE UPDATE");
# The Update-sql-cmd is very useful when we use
# new columns with default value, because the old rows
# will be a null-values.

# inside: context.configure(...) we add: compare_type=True,
# for offline only.

# To Run Workers using rq:
# rq worker -u redis://localhost:6379 emails
# where emails: is the queue name.