FROM colserra/light-encoder:libfdk-aac
WORKDIR /bot
RUN apt-get update
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt install -y aria2
COPY . .
CMD ["bash","start.sh"]
