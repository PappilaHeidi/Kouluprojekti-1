# Jupyter Dockerfile
FROM jupyter/scipy-notebook

# Set working directory
WORKDIR /home/jovyan/work

COPY ./requirements.txt /home/jovyan/work

#COPY requirements.txt /home/jovyan/work/requirements.txt
# Install required packages
RUN pip install -r requirements.txt

# Copy Jupyter content 
COPY .. /home/jovyan/work

# Expose Jupyter Notebook port
EXPOSE 8888

# Start Jupyter Book
#CMD ["jupyter", "notebook", "--NotebookApp.allow_origin=*"]