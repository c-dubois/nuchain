#!/bin/bash
set -e

echo "🔄 Waiting for PostgreSQL..."

while ! python -c "
import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('postgres', 5432))
sock.close()
sys.exit(result)
" 2>/dev/null; do
    echo "⏳ PostgreSQL is not ready yet. Waiting 2 seconds..."
    sleep 2
done

echo "PostgreSQL is ready!"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating reactor data (if not exists)..."
python manage.py create_reactors

echo "🚀 Starting Django development server..."
python manage.py runserver 0.0.0.0:8000