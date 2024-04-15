# Streamlit Dockerfile
FROM python:3.11.7

# Set working directory
WORKDIR /code/streamlit

# Copy requirements file
COPY ./requirements2.txt /code/streamlit/

# Install required packages
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements2.txt

COPY .. /code/streamlit

EXPOSE 8501

CMD ["streamlit", "run", "code/streamlit/streamlit.py"]
