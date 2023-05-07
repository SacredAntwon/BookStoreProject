# CPSC_449_Final_Project

# BookStoreProject

### Members

Member One: Steven Burroughs

Member Two: Anthony Maida

### Setting Up Virtual Environment

Step 1) Clone repository and change to the directory where the files were cloned.

Step 2) Create a virtual environment: "python3 -m venv env"

Step 3) Activate virtual environment: "source env/bin/activate"

Step 4) Install all libraries in the requirements.txt: "pip3 install -r requirements.txt"

### Uploading json to MongoDB

Step 1) Have MongoDB and MongoDB Compass installed

Step 2) Start MongoDB by typing `brew services start mongodb-community@6.0`.

Step 3) Launch MongoDB Compass and connect to the Database.

Step 4) Create a new database by pressing the `+` button.

Step 5) The Database Name is `bookstore` and Collection Name is `books`

Step 5) Once you have it created, click on the books collection and click `Add Data`. Select `Import JSON or CSV file` and locate the file name in the project directory called `sample_books.json`. Confirm by clicking `import` and the data should be inside the database.

### Running the Code

Step 1) Open a terminal window in the same directory as the project files.

Step 2) type `uvicorn main:app --reload` and press enter.

### Using FastAPI Docs to Test

Step 1) Locate the function name of the API endpoint you wish to test

Step 2) Navigate to http://localhost:8000/docs and fill in the required
fields in order to test the API functionality.

Step 3) Look at the MongoDB database to find the Ids for certain books.
