# Streamlit Dockerfile
FROM python:3.11.7

# Set working directory
WORKDIR /code/streamlit

COPY ./requirements2.txt /code/streamlit

#COPY requirements.txt 
# Install required packages
RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements2.txt


# Streamlit port
EXPOSE 8501

# Streamlit
CMD ["streamlit", "run", "streamlit.py"]

