# Word Comparator API

This project implements a word comparator API with two endpoints using FastAPI, RabbitMQ, and Celery. The API allows users to submit a comparison request, which returns a list containing all words that share the same permutation, and get the statistics of the system using a separate stats endpoint.

## Technologies Used

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
- RabbitMQ: A message broker that enables communication between the API and the Celery worker.
- Celery: A distributed task queue system for asynchronous processing.