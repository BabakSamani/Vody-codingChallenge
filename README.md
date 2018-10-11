First setup the environment by installing required python3 packages by running the following command:

``` bash install.sh```

The RESTful API:

Action	HTTP Verb	Description
-----------------------------------------------------------------------------
Create	POST	    Create a new, unique thing
Read	GET	        Read the information about a thing or collection of things
Update	PUT	        Update the information about an existing thing
Delete	DELETE	    Delete a thing


For this project only Read action with HTTP GET request is implemented.

Test links:```
http://127.0.0.1:5000/movie/5bbd685560e7e317c45e1c87
http://127.0.0.1:5000/search/query=100%20Men
http://127.0.0.1:5000/search/query=release%20year:2013 ```
