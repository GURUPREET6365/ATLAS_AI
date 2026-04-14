#!/bin/sh
set -e
# set e is used that if there is any error occurs then terminate the execution.


echo "Print starting command"

alembic upgrade head

echo "Created tables"

python3 -m ATLAS_API.app.frontend_endpoint.utilities.create_admin

echo "Created admin"

exec uvicorn ATLAS_API.app.main:app --host 0.0.0.0 --port 8000
