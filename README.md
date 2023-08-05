# Word Comparator API

This project implements a word comparator API with two endpoints using FastAPI, RabbitMQ, and Celery. The API allows users to submit a comparison request, which returns a list containing all words that share the same permutation, and get the statistics of the system using a separate stats endpoint.

## Technologies Used

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
- RabbitMQ: A message broker that enables communication between the API and the Celery worker.
- Celery: A distributed task queue system for asynchronous processing.
- Redis: A persistent database for storage of word collection along with permutations.

## Installation 

1. Clone the repository (Make sure you have access permissions since this is a private repository)

```bash
git clone https://github.com/itayishr/Gutsy_Task.git
```

2. Install Docker and docker-compose on machine.
3. Build the docker environment:
```
cd Gutsy_Task
docker-compose build
```
4. Run the docker containers:
```
docker-compose up -d 
```

## API Endpoints

### Similar 

#### Endpoint: 
```GET /similar```

#### Description: 
Given a word, returns a list with words that are permutations. 

#### Request URL: 

http://localhost:8000/api/v1/similar?word_to_compare=related

#### Request Body: 

Empty (word is passed as a URI parameter)

#### Response Body:

```json
{
  "similar": [
    "alerted",
    "altered",
    "delater",
    "latrede",
    "redealt",
    "treadle"
  ]
}
```

### Stats 

#### Endpoint: 
```GET /stats```

#### Description: 
Returns application statistics.

#### Request URL: 

http://localhost:8000/api/v1/stats

#### Request Body: 

Empty

#### Response Body:

```json
{
  "totalWords": 150000,
  "totalRequests": 3,
  "avgProcessingTimeNs": 6266205
}
```
## Access the Swagger documentation:

Open your web browser and visit http://localhost:8000/docs to access the Swagger documentation for the API. 
You can explore the available endpoints, make requests, and view responses directly from the Swagger UI.


# Development

The API layer is implemented using FastAPI, which provides a simple way to define routes and request handlers.
RabbitMQ is used as the message broker to facilitate communication between the API and the Celery worker.
Celery is used to handle the asynchronous processing of dictionary processing during first use.

Redis is used as a database which holds the entire dictionary, represented in a key-value manner.
When application initializes for the first time, dictionary is stored in the following manner:
1. Each word parsed from the `words_clean.txt ` file is first sorted alphabetically, in ascending order.
2. The stored word serves as a new key, and the value is a list. 
3. If a key is absent in the Redis database, a new one is created, and the associated list starts with the original unsorted word.
If the key already exists, the unsorted word is simply appended to the existing list.

This allows us fast permutation queries, when the sorted word acts as a hash for all permutations.

# License

This project is licensed under the MIT License.
Feel free to copy the code and use it as the README for your project.
