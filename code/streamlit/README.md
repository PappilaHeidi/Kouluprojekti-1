# Dockerfile
Pystytä docker ensimmäistä kertaa

rakenna levykuvat ja kontit terminaalissa
```shell=
docker build -t kamk/streamlit-projekti1 .

# Aja kontti ylös
# Windows-koneet
docker run -it -v "/$(pwd):/app" -p 8501:8501 kamk/streamlit-projekti1 bash

# Tai
docker run -it -v /$(PWD):/app -p 8501:8501 kamk/streamlit-projekti1 bash

# Mac/Linux
docker run -it -v `pwd`:/app -p 8501:8501 kamk/streamlit-projekti1 bash


# Aja kontissa vielä komento
streamlit run streamlit.py
streamlit run code/streamlit/streamlit.py

```