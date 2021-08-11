# Videos Retrieval Application

## Installation
1. Clone this repo
2. Install python (version >=3.6)
3. Create a virtual environment to work on and activate it
```bash
python3 -m venv video_api
source video_api/bin/activate
```
4. Install dependencies
```bash
pip install -r ../requirements/requirements.txt
```
5. open `variables.sh` and input your youtube API keys comma-separated, save the file and source it.
eg:
```bash
export GOOGLE_API_KEYS="key1,key2"
export SECRET_KEY="abc"
export DB_USER=""
export DB_NAME="videoapi"
export DB_PASS=""
export DB_HOST="localhost"
# save and then run
source variables.sh
```
6. install postgresql (you can follow any article over internet to install the latest version)

```bash
# for mac users
brew install postgresql
```
7. open psql terminal and create a db named `videoapi`
```bash
psql
# psql terminal opens
create database videoapi;
# OR directly from shell
psql -c 'create database test;'
```
8. Run all the migrations
```bash
python manage.py migrate
```
9. Setup the cron
```bash
crontab -e
# opens vi editor(or whichever is set as default)
# enter this command in the editor and save it(:wq) [Make sure to leave a new line at EOF else cron will not run]
*/5 * * * * curl --request POST http://localhost:8000/fetch-store-videos/

```
You'll get a confirmation that your cron is set.
  

Note: If you're willing to run the server at a different port please change it.
  
10. Final step, Run the server
```bash
python manage.py runserver # runs on port 8000
```
11. Create super user to access admin dashboard
```bash
python manage.py createsuperuser
```
**The application is accessible at localhost:8000**


## Installation using docker
1. Install docker by clicking [here](https://docs.docker.com/get-docker/)
2. clone this repo
3. Then `cd video-api` and Edit the variables.sh file. 
Here put your environment variables like Google API keys etc.
```bash
export SECRET_KEY="abc"
export GOOGLE_API_KEYS="key1,key2"
export DB_USER="videoapi_user"
export DB_NAME="videoapi"
export DB_PASS="1234"
export DB_HOST="db" # MANDATORY: this needs to be "db" else we need to make a change in docker-compose file
```
4. it's time to create docker image and run your container.
```bash
docker-compose up -d --build
```
5. Now we have to create a cron job that will hit the API `fetch-store-videos` repeatedly after 2 minutes and store the latest 5 records in DB. 
  
    NOTE:     Make sure to install cron job if not present. The below steps are for Linux based systems.
```bash
>>crontab -e
# Editor will open, Copy paste the below cron instruction
*/2 * * * * curl --request POST http://localhost:8000/fetch-store-videos/

# Make sure to leave a newline else cron will not run
# save the changes and provide the password to confirm and Now the cron is up and running.
```
To check whether cron is running or not you can either log inside the container and check the logs at `/tmp/debug.log` or directly check in the host machine `pgrep -u root cron` as cron is being run with root permissions.
Note: To stop the cron just comment out the line which we typed after executing the command `crontab -e`

**The application is accessible at localhost:8000**

## APIs exposed
I've used search query `sports` for getting videos from youtube.
1. `videos` - Gets videos stored in the db in reverse chronological order of publishedAt date time.
  
    Response contains: title, published_at, description and thumbnail_urls

    You can pass `page_number` as query parameter. eg: page_number=2
2. `search-videos` - Pass `search_query` as string stating the words to be searched amongst title and description(partial matching). The results returned are also paginated based on page number.
  
    Handled this specific optimisation:
`Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.`
  
    By using `GinIndex` as it indexes the composite values from title and description and the part of the queries are searched through these composite values in index.

  
    If admin dashboard contained filters(not present in the current application) then we can have indexes based on those filter fields like: video_id, channel_id
  
    NOTE: If `search_query` is not passed then it will return the same result as `videos` API.
