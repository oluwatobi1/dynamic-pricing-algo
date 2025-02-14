# dynamic-pricing-algo
DYNAMIC PRICING ALGORITHM FOR A RIDE-HAILING APP


The Dynamic Pricing API is a Django-based service that calculates ride fares dynamically based on factors such as distance, traffic conditions, demand levels, and time of day.















### Features
- Implements real-time dynamic pricing.
- Factors include:
    - Base Fare
    - Per Kilometer Rate
    - Traffic Multiplier
    - Demand Surge Multiplier
    - Time-of-Day Pricing (Peak and Off-Peak times)
- RESTful API built with Django REST Framework (DRF).
- Swagger UI for API documentation.
- Unit tests with Django's testing framework.


### Technology Stack
Backend: Django, Django REST Framework
Database: SQLite (default, can be changed)
Containerization: Docker 


### Installation & Setup
- Prerequisites
    - Python 3.13+
    - Docker (optional, for containerized setup)

### Setup instructions
1. Clone this repository
2. Navigate to the project directory(dynamic_pricing_project) ie. run `cd dynamic-pricing-algo/backend`
### How to run the application

#### Method 1: Running locally with virtual environment
3. Create a virtual environment. Run `python3 -m venv venv`
4. Activate the virtual environment. Run ` source venv/bin/activate` - (Sample command is for unix based OS)
5. Install the project dependencies. Run `pip install -r requirements.txt`
6. Run Migrations. Run `python manage.py migrate`
7. Run the application. Run `python manage.py runserver`

The API will be available at `http://127.0.0.1:8000/`

#### Method 2: Running with docker
3. Build the docker image. Run `docker build -t dynamic-pricing-algo:latest .`
4. Run the docker container. Run `docker run  dynamic-pricing-algo:latest`


#### Swagger API Documentation
Once the application is running, access API documentation at:
http://127.0.0.1:8000/swagger/
### How to run tests
Test are in the `pricing/tests` directory. 
- To run the tests, run the following command 
 - Navigate to the project directory(dynamic_pricing_project) ie. run `cd dynamic-pricing-algo/backend`
- Run `python manage.py test  ./pricing/tests/**`