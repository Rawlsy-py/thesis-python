# 
FROM python:3.12

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code

EXPOSE 80
# 
CMD ["fastapi", "run", "/code/app/main.py", "--port", "80"]