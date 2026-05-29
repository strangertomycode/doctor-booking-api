FROM python:3.12-slim

WORKDIR /app

# install uv
RUN pip install uv

# copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# create venv + install dependencies
RUN uv sync --frozen --no-install-project

# copy project
COPY . .

# IMPORTANT: use uv's venv python
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# run migrations + gunicorn
CMD sh -c "python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"