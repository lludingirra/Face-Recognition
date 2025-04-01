# Face Recognition Attendance System

## Requirements

Before running the project, ensure that the following libraries and tools are installed:

- Python 3.x
- OpenCV
- dlib
- face_recognition
- pickle
- datetime
- numpy
- cvzone
- sqlite3

Once you’ve confirmed that the necessary libraries are installed, place images of the individuals you want to detect inside the **images** folder. These images should have dimensions of (216, 216, 3). Afterward, update the table in the `AddDataToDatabase.py` file according to your preferences.

### Column Descriptions

The following columns in the database are used to track student information and attendance:

- **id**: A unique identifier for each student.
- **name**: The student's full name.
- **major**: The student's department or field of study.
- **starting_year**: The year the student enrolled in the university.
- **total_attendance**: The total number of attendances recorded for the student.
- **standing**: The student's academic status (e.g., Pass, Fail).
- **year**: The student's current academic year (e.g., 1st year, 2nd year, etc.).
- **last_attendance**: The timestamp of the student's most recent attendance (e.g., '2023-10-15 12:37:00').
- **image**: The student’s face image stored in the database (optional).

Feel free to modify and customize these columns according to your needs.

## Setting Up and Running the System

1. First, run the `AddDataToDatabase.py` file. This will create a `.db` database file in your project directory.

2. Next, run the `EncodeGenerator.py` file. This will generate a file named `EncodeFile.p` in your directory, which contains the encoded face data.

3. Finally, run the `main.py` file to launch the Face Recognition Attendance System.

After following these steps, the system will be ready to detect faces and record attendance based on the images and data you've provided.
