# Implemented functionalities

* As a developer I want to store all data in a relational database,
* As a user I want to have an API endpoint for retrieving all lectures with the ability 
to paginate the results,
* As a user I want to have an API endpoint for querying lectures by author's name,
* As a content provider I don't want users to see my lectures if they've been rated 
lower than a system-wide average,
* As a code reviewer I want to have an easy way of spinning up the project and running test 
requests against the provided API endpoints.


# In progress

* As an admin I want to have an API endpoint to batch load the seed data into a
database,


# Not Implemented (with a description of how I would do it)

* As a user I want to have an API endpoint for querying lectures by tags
  * How I'd do it:
    * add support for another query param (filter[tags]=tag1,tag2)
    * add tags table to DB with:
        * ID of type UUID
        * name of type VARCHAR
    * add lecturetotags table to DB with
        * ID of type Integer
        * lectureId of type UUID (foreign key)
        * tagId of type UUID (foreign key)
    * add logic
* As a user I want to have an API endpoint for retrieving top 10 highest rated lectures,
  * How I'd do it:
    * add another endpoint /lectures/top with support for limit query param (it may have a default value of 10
    and not accepting value above some defined value, may be as well 10)
* As a user I want to have a "feeling lucky" API endpoint for retrieving a random
lecture, but I don't want to see the same lecture twice in a row,
    * How I'd do it:
      * add endpoint /lectures/random
      * get random number within range [0, lectures_count) which would be used to choose the lecture
      * set Cache-Control: no-store response header


# Launching services
docker-compose up -d
  * I have a problem that backend service for some reason is not connected to the docker network at the first 
  run. I haven't looked into that so far so current workaround is to run docker-compose up for the second time

The .env files are committed to the repo for convenience  