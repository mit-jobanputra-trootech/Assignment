Requirements:
- Create 2 microservices. 
- Each microservice has their own database.
- From microservice A call microservice B to save data and fetch data.
- Use one encryption method to save password.
- Use validation for payload

-----------------------------------------------------
Technologies:
- Microservice Framework: FastAPI
- ORM : Sqlalchemy
- Migration : Alembic
- Payload Validation: Pydantic
- Authentication: OAuth 2
- Password Encryption: sha512

--------------------------------------------------------
Steps for setup microservice:
- Setup virtualenv and install requirements 
  - pip install virtualenv
  - source env/bin/activate
  - pip install -r Microservice-A/requirements.txt
- create two databases with name micro_a, micro_b
- create .env file with below variable for Microservice-A
  - DATABASE_URL
  - SECRET_KEY // for authentication token 
  - ALGORITHM  // for authentication token 
- create .env file with below variable for Microservice-B
  - DATABASE_URL
  - MICROSERVICE_A_ENDPOINT
- command to run microservice-A in local:
  - uvicorn main:app --reload --port 8000
- command to run microservice-B in local:
  - uvicorn main:app --reload --port 8001
-Access docs URL:
  -  http://localhost:8000/docs
  -  http://localhost:8001/docs
- Endpoints:
  - From Microservice-B call Microservice-A endpoints
    - /api/v1/users/register - Insert user details in DB
    - /api/v1/users/login - Generate the access token
    - /api/v1/users/listing - Fetch the user listing