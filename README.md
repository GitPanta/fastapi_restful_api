# RESTful API implementation for Electoral System

RESTful API implementing the D'Hondt electoral system.


## Before you start
Some considerations to keep in mind before trying the app:

- This guide assumes you are using windows powershell terminal.
- There is some sensible data inside the `.\app\core\config.py` file, like a secret key and the sql uri. You should remove the values from that file and create a `.env` file in the root folder with them (use the same names).
- You need a user for performing any significant operation.
- A couple of entities are created on startup: a superuser (check credentials on the config file), an election, and five candidate rosters.
- An overview of the endpoints is provided below, but you should check the specific of each endpoint on the generated documentation (the `/docs` url).
- Elections, users, and rosters entities have the field `is_active` which is only implemented on elections. The value on the other entities have no effect whatsoever.

## Running the APP
You can run the app either with Docker or with a virtual environment.

Once the ap is running, you can test it with Postman or going to `localhost:8000/docs` (runing from virtual environment) from a browser.

### Docker

Keep in mind that a persitent database is not implemented in docker. If you want the database to be persistent, run the app with a virtual environment.

For running the app in Docker, follow the steps:

1. Open a terminal on the root folder.
2. Run the command `docker build -t imagename` wait for the image to be created.
2. Run `run -d --name containername -p 80:80 imagename`.
3. The app should be now running in `localhost:80`.

### Virtual environment

1. Open a terminal on the root folder.
2. Run `python -m venv venv` to create the virtual environment.
3. Activate it running `venv\Scripts\activate`.
4. Install the required packages running `pip install -r requirements.txt`.
5. Move to the app folder with `cd .\app\`.
6. Run `fastapi run .\main.py`.
7. The app should be running at `localhost:8000`.


## Security
The app implements JSON web tokens using the OAuth2 specification. You can login on the `/login` endpoint to get the token.

There are three levels of permission:

1. User: can access the `/users/me` endpoint to get the current user information, but no additional permissions are implemented.
2. Admin: can use any endpoint except for creating users.
3. Super admin: allowed to all endpoints.

You can create more users using the `/users` endpoint.


## How to use

First login using an admin level user on the `/login` endpoint. There should already be an election created and five rosters in place, but you can create your own using the `/elections` and `/rosters` endpoints, respectively.

Additionally, you can also get a list of the existing elections/rosters using those enpoints, which is usefull for setting seats and handling records since the IDs are required.

The elections holds a description, the amount of seats to dispute, and a field named `is_active` used to end the electio count, while the rosters are just the names. You can set the amount of seats on an existing election on the `/elections/seats` endpoint.

Rosters can exists on their own. They relate to an election with the records entity. A record holds the amount of votes the roster got for the respective election and the amount of seats it acquired (only available after the election count has ended).

Use the `/records` endpoint to create the records. It requires the election ID and roster IDs, as well as the amount of votes received by each roster. You can also modify a single record with a PUT request to the same endpoint, but it needs to already exists.

Once all records have been created, use the `/elections/end` endpoint to finish the election and get the results with the amount of votes and seats of each roster.

You can always get the results of a particular election using the `/records/{election_id}` endpoint (replace `election_id` by the ID of the election you want to check), or you can get all existing results with a GET request to the `/records/` endpoint.