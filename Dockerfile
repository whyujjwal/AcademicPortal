
FROM python:3.10



ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1


WORKDIR /app

#nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


#psycopg2 dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

    
#build installations
RUN pip3 install --upgrade pip 
COPY pipfile* ./
COPY requirements.txt .
RUN pip3 install -r requirements.txt




COPY . .



COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
