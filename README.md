A RESTful API to get movie/show media type:
-----------------------------------------------------------------------------------------------------
This API is written in Python and uses MongoDB as its database to store data of show or movie medias. 
For this project only GET method of the RESTful API is implemented.

```
Action	HTTP Verb	Description
_______________________________________________________________________________

Read	GET         Read the information about a media or collection of medias.
 ```
 
Instruction for using this API
-----------------------------------------------------------------------------------------------------
Please visit the home page of the API for more information about how to use this API.

Data
-----------------------------------------------------------------------------------------------------
The data for this api is extracted by using the following source:
``http://www.omdbapi.com/`` 

Set up the API
-----------------------------------------------------------------------------------------------------
For security reasons, an environment file called ``.env`` is setup to store usernames, passwords, API 
keys and etc. 
First you need to setup this file on your server in the same directory of this application. 
The following are the variables that should be in the ``.env`` file:

```bash
MONGO_DB_HOST=
MONGO_DB_PORT=
MONGO_DB_NAME=
MONGO_COLLECTION=

MEDIA_API_URL=http://www.omdbapi.com/?apikey=<key>&t=<media_title>

HOST_IP=
HOST_PORT=
```
A bash file is written to install required python packages, Mongodb, then get the test data from 
the API and run the server. By running the following command all above processes will be 
automatically executed:

``` bash install_run.sh```

Setup database from backup file
-----------------------------------------------------------------------------------------------------
Also, there is a backup for the database that you can run and load the data into the database by 
following command:
```
mongorestore -d <database_name> /data/Vody/
```


Test links:
```
http://142.93.195.130/api/<user_token>/movie/5bbd685560e7e317c45e1c87
http://142.93.195.130/api/<user_token>/search/query=100%20Men
http://142.93.195.130/api/<user_token>/search/key=release%20year&value=2013 
```
