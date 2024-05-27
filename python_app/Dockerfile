FROM python:latest



WORKDIR /usr/src/app


COPY . .

RUN pip install mysql-connector-python

# Copia el script wait-for-it.sh
COPY wait-for-it.sh /usr/src/app/wait-for-it.sh

RUN pip3 --no-cache-dir install -r requirements.txt

# Dale permisos de ejecución al script wait-for-it.sh
RUN chmod +x /usr/src/app/wait-for-it.sh

CMD ["/usr/src/app/wait-for-it.sh", "db:3306", "--", "python", "app.py"]