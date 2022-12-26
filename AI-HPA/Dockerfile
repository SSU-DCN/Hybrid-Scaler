FROM ubuntu:18.04
RUN apt update && \
      apt install -y curl && \
      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl
RUN apt install -y python3-dev python3-pip python3-venv && pip3 install --upgrade pip

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py"]
