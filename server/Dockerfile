FROM python:3.9-alpine

RUN mkdir /service
WORKDIR /service


# Requirements
ADD requirements.txt ./
RUN apk add git && \
    pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

# Source
ADD . ./server/

# Run
EXPOSE 8000
CMD ["uvicorn", "server.api:app", "--host", "0.0.0.0", "--port", "8000"]
