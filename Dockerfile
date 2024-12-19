FROM apache/spark:3.5.0

WORKDIR /app

USER root
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install flask==3.0.1 pyspark==3.5.0 flask-cors==4.0.0
USER spark

COPY api.py .
EXPOSE 5001

CMD ["python3", "api.py"]
