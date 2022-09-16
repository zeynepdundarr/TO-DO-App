# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

## for todo-app uncommet below
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
## for test uncommet below
# CMD pytest app/tests