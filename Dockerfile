FROM python

WORKDIR /atlas_ai

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "docker_command.sh"]
