FROM python:3.10-slim

# 
WORKDIR /app

# 
COPY ./requirements.txt /app

# 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg
RUN apt-get -y update && apt-get install -y libsndfile1

# 
COPY . .

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
