from flask import Flask, render_template, request
import os
import boto3

app = Flask(__name__)

# Fetching environment variables or setting default values
DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT"))

# AWS configuration
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION") or "us-east-1"
BUCKET_NAME = os.environ.get("BUCKET_NAME") or "clo835-project"
IMAGE_NAME = "download.jpg"  # Replace with your actual image name
IMAGE_DIRECTORY = "images"

# Define the download_image function
def download_image(bucket_name, directory, image_name):
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        s3 = session.resource('s3')
        image_path = f"/tmp/{image_name}"
        s3.Bucket(bucket_name).download_file(f"{directory}/{image_name}", image_path)
        return image_path
    except Exception as e:
        print("Exception occurred while fetching the image:", e)
        return None

# Fetch image from S3 bucket
image_path = download_image(BUCKET_NAME, IMAGE_DIRECTORY, IMAGE_NAME)

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
