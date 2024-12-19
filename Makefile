all: build start

build:
	docker build -t spark-container .

start:
	docker run -d -p 5001:5001 -p 8080:8080 -p 4040:4040 -p 7077:7077 spark-container
