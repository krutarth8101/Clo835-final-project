from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import os
import boto3

app = Flask(__name__)

# Fetching environment variables or setting default values
DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT"))
BGIMG = os.environ.get("BGIMG") or "download.jpg"
BUCKETNAME = os.environ.get("BUCKETNAME") or "clo835-project"

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD, 
    db=DATABASE
)

output = {}
table = 'employee';


bucket = "clo835-project"
image = "download.jpg"

@app.route("/download", methods=['GET', 'POST'])
def download(bucket=bucket, imageName=image):
    try:
        imagesDir = "temp"
        if not os.path.exists(imagesDir):
            os.makedirs(imagesDir)
        bgImagePath = os.path.join(imagesDir, "image.png")
        s3 = boto3.resource('s3')
        s3.Bucket(bucket).download_file(imageName, bgImagePath)
        return os.path.join(imagesDir, "image.png")
    except Exception as e:
        print("Exception occurred while fetching the image! Check the log --> ", e)


# Fetch image from S3 bucket
image_path = download(bucket, image)

# Route for the home page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image_path=image_path)

# Route for the about page
@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', image_path=image_path)

# Route for adding employee information
@app.route("/addemp", methods=['POST'])
def AddEmp():
    # Add employee information to the database
    # Retrieve form data and perform database operations
    # Add your implementation here
    return render_template('addempoutput.html', name=emp_name, image_path=image_path)

# Route for getting employee information
@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", image_path=image_path)

# Route for fetching employee data
@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    # Fetch employee data from the database
    # Retrieve form data and perform database query
    # Add your implementation here
    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], image_path=image_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
