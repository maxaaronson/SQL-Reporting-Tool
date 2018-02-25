# NEWS DB REPORT TOOL
This python program will perform several queries on the ```news``` database and display the outputs.

## Installation
##### Required environment:
- python 3 interpreter installed
- PostgreSQL installed with a database called ```news``` 

##### Required python modules:
- psycopg2
- psycopg2.extras

##### Required sql file:
- the news.sql file must be run to populate the ```news``` database.  It can be found at https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
- run the file with ```psql -d news -f newsdata.sql```

##### To run:
- Run ```"NewsReportTool"``` from the command line
        