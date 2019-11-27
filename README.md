# dma-student-information-system
This is a Student Information System that provides various modules to manage the administrative tasks of a College.

### Getting Started

1. Ensure that python3 and postgresql is installed.

2. Create a postgres role called 'dhaval' with password 'dhaval'. Create a database called `student_information_system`. Remember to grant all privileges to 'dhaval';

3. Install `virtualenv`.

4. On Linux, run `virtualenv venv` where `venv` is the folder that will contain the packages and what not to run the app. Then `source venv/bin/activate` to enable that virtual environment.

5. Install the necessary packages in the virtual environment with `pip install -r requirements.txt`.

6. Create the necessary tables with `python manage.py makemigrations && python manage.py migrate`.

7. Initialize data with the following commands, in order:

  a. `python manage.py initgroups`

  b. `python manage.py initcurriculum`.

  c. `python manage.py createumuser`.

  d. In case monthly attendance needs to be created, create it with `python manage.py createmonthattendance _course_ _semno_`

8. Run with `python manage.py runserver 0.0.0.0:8000`
