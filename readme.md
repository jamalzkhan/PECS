# PECS (Peformance Evaluation of Cloud Services)

- Final year MEng Computing project at Imperial College London by Jamal Khan, jzk09@doc.ic.ac.uk

## Service time evaluation time installation

The service evaluation tool was tested out in the Mac OS X Mountain Lion and Ubuntu 12.04 operating system distributions. To run the tool you must have the following dependencies installed (most are available by default):

- Python
- Git (for checking out the code)
- PostgreSQL
- MongoDB
- Node.js

For Python we need to additionally install the twython, pymongo, psycopg2 libraries. For Node.js we just need the express library. Also ensure that you have the libpq-dev and python-dev libraries installed on your machine.

The code can be checked out from https://github.com/jamalzkhan/PECS.git, to start using the tool go into the main directory and carry out the following commands:

> cd peformance_framework
> mkdir logs

You also need to configure the config.conf file with information such as your Twitter API access tokens. An example configuration file has already been created in the code base (conf_example.conf) but requires editing. Please refer to below to setup the configuration file for database or HTTP web server evaluations respectively.

## Running database evaluations

Before beginning to use the tool please ensure that the PostgreSQL or MongoDB server is running to avoid any exceptions.

If you are using the tool for evaluating performance of PostgreSQL databases then you should create a database and a new user.

> sudo -u postgres createuser --superuser $USER   
> sudo -u postgres createdb performance

The following should be included in your configuration file if you want to conduct a database evaluation.

- Twitter API access tokens
- Postgres username and password
- Database and table name that will be used by the evaluation tool. Please do not use an existing table name if you want to use it for purposes other than this profiling tool, Unless you really know what you are doing!

For PostgreSQL to create a table automatically you can carry out the following command:

> Python Performance.py -d postgres -c

The following database specific flags are used by the tool:

* -d database_name (Use either postgres or mongo)
* -i inserts (Number of write operations to carry out)
* -s selects (Number of read operations to carry out)
* -c (Automatically create a table, only use with the -d postgres flag)

An example usage of the tool is:

> Python Performance.py -d postgres -i 200 -s 300

This will insert 200 Tweets into the specified PostgreSQL instance and also carry out 300 read operations on the table where the Tweets are stored.

All the response times for the tool are stored in the "logs/" folder.

## Running HTTP web server evaluations
Please ensure that a web server is switched on if you want to conduct performance evaluation for a HTTP web server.

The following should be included in your configuration file if you want to conduct a HTTP web server evaluation.

- The URL to which you want to POST data to and also the URL you want to perform GET requests to
- Post data that you would like to send to the web server when conducting POST requests

The following web server specific flags are used by the tool:

* -u url (URL of the web server, e.g. localhost)
* -p port (Port at which the webserver is operating)
* -g gets (Number of GET requests to perform)
* -x posts (Number of POST requests to perform)
* -n threads (Number of concurrent connections to make)

The tool will conduct the post request and get requests multiplied by the concurrent connections. An example usage is:

> python Performance.py -u localhost -p 80 -g 3000 -x 2000 -n 30

This performs 3000 GET requests and 2000 POST requests multiplied by 30 concurrent threads on the localhost HTTP web server at port 80.

Also note that the Node.js webserver in the code base has a GET and POST method implemented in the "/" and"/posturl"  path respectively, so you can use this as a starting point.

## Chart data

Data used for chart creation in the report is in the analysis/ folder and some helper Matlab files are there as well.

## Cloud computing setup

Some sample configurations that were used in Java Modelling Tools are in the jmt/ folder. They can be directly loaded into the tool for analysis.

