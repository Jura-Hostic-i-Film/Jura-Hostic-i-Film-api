# Jura-Hostic-i-Film-api

## Description
This is the REST API for the "Digitalizacija" app. You can access the mobile app repository [here](https://github.com/Jura-Hostic-i-Film/Jura-Hostic-i-Film-app).
The project aims to help digitization of documents using OCR technology and make the process of managing documents easier.

## Installation
1. Install python 3.11 https://www.python.org/downloads/
2. Clone the repository using `git clone https://github.com/Jura-Hostic-i-Film/Jura-Hostic-i-Film-api.git`
3. Install the required python packages using `pip install -r requirements.txt`
4. (Optional) Create a `.env` file in the root directory and add some or all of the following variables:
    ```
    SECRET_KEY=<your_secret_key>
    ACCESS_TOKEN_EXPIRE_HOURS=<your_access_token_expire_hours>
    DATABASE_URL=<your_database_url>
    AccountKey=<account_key>
    AccountName=<account_name>
    DefaultEndpointsProtocol=<default_endpoints_protocol>
    EndpointSuffix=<endpoint_suffix>
    vision_endpoint=<vision_endpoint>
    vision_key=<vision_key>
    image_path=<image_path>
    ``` 
5. Run the server using `uvicorn app.main:app --reload` and the server will be available at the link provided in the terminal

## Usage
The API is documented using Swagger and you can access the documentation at the `/docs` endpoint.

## Deployed version
The API is deployed on render.com and you can access it [here](https://jura-hostic-i-film-api.onrender.com/docs).
