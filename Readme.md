# Todo-App 📝 

## Project Description

Todo-App is an app in which user can create their own accounts and create their own todo's. Users can save, categorize, prioritize and schedule their todo's. 

### Technology

- Todo-App is implemented in FastApi web framework.
- SQLAlchemy is used for SQLite database communication. 
- Docker is used for standardizing the application by including the everything that software needs.

## Deployment with Docker

Docker should be installed in your computer to continue with deployment.
In order to build the app you should: 

```bash
git clone https://github.com/zeynepdundarr/TO-DO-App.git
cd TO-DO-App/app
docker build -t <image-name> .
docker run -p <local-port-number>:8080 zeynep
```

You should enter address [http://localhost:{your_port_number}/docs](http://localhost:<local-port-number>/docs) to use Todo-App. 


## Run Tests
Tests can be found in the tests/ folder in app/ directory.

In order to run the test suit you should run the commands below.
```bash
git clone https://github.com/zeynepdundarr/TO-DO-App.git
cd TO-DO-App
pip install -r requirements.txt
cd app
pytest tests/
```

## Web Routes
All routes can be accessed on /docs or /redoc paths with Swagger or Redoc.

