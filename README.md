# dynamic-pricing-algo
DYNAMIC PRICING ALGORITHM FOR A RIDE-HAILING APP












### Setup instructions
1. Clone this repository
2. Navigate to the project directory(dynamic_pricing_project) ie. run `cd dynamic-pricing-algo/dynamic-pricing-project`
### How to run the application

#### Method 1: Running locally with virtual environment
3. Create a virtual environment `python3 -m venv venv`
4. Activate the virtual environment. ` source venv/bin/activate` - (Sample command is for unix based OS)
5. Install the project dependencies `pip install -r requirements.txt`
6. Run the application `python manage.py runserver`

#### Method 2: Running with docker
3. Build the docker image `docker build -t dynamic-pricing-algo:latest .`
4. Run the docker container `docker run  dynamic-pricing-algo:latest`

### How to run tests
Test are in the `pricing/tests` directory. 
- To run the tests, run the following command
- `python manage.py test`