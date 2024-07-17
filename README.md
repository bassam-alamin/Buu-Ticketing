# Ticketing-template 
Ticketing APP

VERSIONS:

PYTHON 3.11

Prerequisites:
1. Make sure you have postgresql and redis installed on your machine

2. Create a database that you will replace it on the .env

How To Run:
1. Download all requirements from the requirements.txt file
    ``` pip install -r requirements.txt```

2. Copy contents of .env.example to your .env file and replace with the respective details
    ``` cp .env.example .env```

3. Run the server locally
    ```python manage.py runserver```

4. Run migrations
    ``` python manage.py migrate```

5. Start Celery Worker
    ``` celery -A ticketing worker -l INFO```

6. Start Celery Beat
    ``` celery -A ticketing beat -l INFO```


To view Api endpoints:
On Your browser enter
 [127.0.0.1:8000/developer/docs](http://127.0.0.1:8000/developer/docs)

 
<img width="1367" alt="Screenshot 2024-07-17 at 01 56 15" src="https://github.com/user-attachments/assets/17007873-06af-4955-9fcb-8cf447fbdd4b">

To run tests:
    ```python manage.py test```

Or run specific app tests:
    ```python manage.py test app_name```


HOW TO TEST STEP-BY-STEP:

ADMIN:

1. Open terminal on root folder and create superuser (This is the user that will be able to create Theatres and Seatings)
    ``` python manage.py createsuperuser```
   
2. Use the login endpoint to obtain JWT token.
<img width="1367" alt="Screenshot 2024-07-17 at 09 08 51" src="https://github.com/user-attachments/assets/a0d6ff9e-718f-407b-baed-e2d9bb9e5efb">

3. Copy the jwt token and paste on the authorization button with Prefix "Bearer .....".
<img width="1367" alt="Screenshot 2024-07-17 at 09 11 47" src="https://github.com/user-attachments/assets/e2d36d30-ce07-403a-87b2-3901157c1fa6">
  
4. Now you can start creating theatres.
<img width="1359" alt="Screenshot 2024-07-17 at 09 13 16" src="https://github.com/user-attachments/assets/3212d14f-c3d9-4c0f-a650-0ca6a6088540">

5. Now the admin can create a seating.
<img width="1359" alt="Screenshot 2024-07-17 at 09 14 01" src="https://github.com/user-attachments/assets/fca1ffd0-4b25-4d07-9714-366ad5a11162">

6. Finally admin can view reservation details.
<img width="1346" alt="Screenshot 2024-07-17 at 09 15 04" src="https://github.com/user-attachments/assets/f62034cd-3c4e-4f85-9707-2f5904f3fb3e">

