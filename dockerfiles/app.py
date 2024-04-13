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
        imagesDir = "static"
        if not os.path.exists(imagesDir):
            os.makedirs(imagesDir)
        bgImagePath = os.path.join(imagesDir, "image.jpg")
        s3 = boto3.resource('s3')
        s3.Bucket(bucket).download_file(imageName, bgImagePath)
        return os.path.join(imagesDir, "image.jpg")
    except Exception as e:
        print("Exception occurred while fetching the image! Check the log --> ", e)


# Fetch image from S3 bucket
image = download(BUCKETNAME, BGIMG)

# Route for the home page   
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=image)

# Route for the about page
@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', image=image)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form.get('emp_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    primary_skill = request.form.get('primary_skill')
    location = request.form.get('location')

    if not emp_id or not first_name or not last_name:
        # If any of the required fields are missing, return an error response
        return "Error: Employee ID, first name, and last name are required.", 400

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"  # Use f-string for concatenation

    finally:
        cursor.close()

    print("All modifications done...")
    image = download(BUCKETNAME, BGIMG)
    return render_template('addempoutput.html', name=emp_name, image=image)


@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    image = download(BUCKETNAME, BGIMG)
    return render_template("getemp.html", image=image)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id))
        result = cursor.fetchone()
        
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    image = download(BUCKETNAME, BGIMG)
    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], image=image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
