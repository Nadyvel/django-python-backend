# Pull miniconda from docker hub as base image
FROM continuumio/miniconda3:latest

# Copy the requirements file from local folder to image
COPY ./motion_scratch/requirements.yml /motion_scratch/requirements.yml

# create the environment inside the docker container
RUN conda env create -f /motion_scratch/requirements.yml
RUN mkdir /scripts
RUN mkdir /static-files
RUN mkdir /nginx
# we set the path were all the python pacakages are
ENV PATH /opt/conda/envs/motion-scratch/bin:$PATH

# activate app
RUN echo "source activate motion-scratch" >~/.bashrc

# pass all the files and folders from local folder to image
COPY ./motion_scratch /motion_scratch


# pass the script (skip that step if you don't have any scripts)
COPY ./scripts/* /scripts/
RUN chmod +x /scripts/*

RUN echo "source activate motion_scratch" >~/.bashrc
# set the working directory to /app for whenever you login into your container
WORKDIR /motion_scratch

# '/motion_scratch' can be named differently. this is the main folder for your backend app