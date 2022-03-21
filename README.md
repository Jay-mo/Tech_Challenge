# CNS Tech Challenge

## Getting Started

This is a web service that receives GET requests from a web proxy with hostname and port numbers and must give a response back to the proxy, whether or not to allowed traffic 
to the provided hostname and port number. There are also two endpoints used to list all the urls in the database and also to update the database with new urls.

### Installing Dependencies

#### Docker

Follow instructions to install the latest version docker for your platform in the [docker docs](https://docs.docker.com/)

#### Docker-Compose

Docker compose is used to automate the setup of the containers. More information can found in the [docker docs](https://docs.docker.com/compose/)


##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Mongodb](https://www.mongodb.com/) and [Mongoengine](http://mongoengine.org/) are libraries to handle the NoSQL database. 

- [Nginx](https://www.nginx.com/) is the load balancer used to share load across the flask application servers.




## Running the docker environment

Once you install docker and docker compose, from within the  working directory run the following command


```bash
docker-compose up 
```

To scale the number of application servers run the following

```bash
docker-compose up --scale flask=2
```


### Endpoints 
#### GET /urlinfo/1/{string:hostname_and_port}/{string:original_path_and_query_string}
- General:
    - Returns the hostname, port number and the block status of the submitted url. 
- Sample: `curl localhost:80/urlinfo/1/youtube.com:9091/youtube.com:9091?video=john&rating=1000/`

``` {
  "block_status": false, 
  "hostname": "youtube.com", 
  "port": "9091"
}
```



#### GET /urlinfo/1/url_db
- General:
    - Returns a list of url names, port numbers, and block statuses from the url database.
    
- Sample: `curl localhost:80/urlinfo/1/url_db`

``` [
  {
    "block_status": true, 
    "port": 9091, 
    "url": "yahoo.com"
  }, 
  {
    "block_status": true, 
    "port": 9333, 
    "url": "cnn.com"
  }
]
```


#### POST /urlinfo/1/<string:hostname_and_port>
- General:
    - Creates a new url entry in the url database. Returns the success value. 
- Sample `curl -X POST localhost:80/urlinfo/1/youtube.com:9091`
```
{
  "success": true
}
```