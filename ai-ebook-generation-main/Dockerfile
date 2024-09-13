FROM python:3.7

WORKDIR .

RUN apt-get update

COPY . . 

RUN (find . -name "requirements.txt" -exec pip3 install -r {} \;)

# CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8000"]