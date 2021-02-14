#### Install Project Prerequisites (On windows)
##### Install Python
- check version if installed (python -V)
- otherwise follow the steps from https://www.python.org/downloads/

##### Install pip
- follow the steps from https://www.liquidweb.com/kb/install-pip-windows/

##### Install Latest Version of Django
- Follow the steps from https://docs.djangoproject.com/en/3.1/topics/install/

#### How to run this project
##### Create Virtual Env 
```
pip install virtualenvwrapper-win
mkvirtualenv my_django_environment
```

##### Install Project Requirements
```a
pip install -r requirements.txt
```

```
python manage.py createsuperuser
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```

```
python manage.py runserver
```

###### Login as superuser
http://127.0.0.1:8000/admin

- [Create an application here](http://127.0.0.1:8000/o/applications/) by providing below information
    - Name -- APP_NAME from [Here](library_management/config.py). You can change APP_NAME too.
    - Client type -- ```Confidential```
    - Authorization grant type -- ```Resource owner password-based```
- [Create two Groups from here](http://127.0.0.1:8000/admin/auth/group/add/) according to following
    - name = LIBRARY_ADMIN and MEMBER from [Here](library_management/config.py)
    - Permissions not needed to be added as we are working with static permissions here.
    

##### Sign up/Sign In for a library Admin
- using ```'/email-signup'``` api and providing necessary information (Example: [Here](Resources/API Collections/library_management.json))
- This account need to be authorized by superadmin first which can be done by following two ways
    1. Login to admin site and go [here](http://127.0.0.1:8000/admin/users/profile/) click on the user and ```make is_authorized checked, Groups=library_admin and save```
    2. Collect Client_id and secret from [here](http://127.0.0.1:8000/o/applications). And Use ```/o/token/``` provide necessary information for superuser. (Example: [Here](Resources/API Collections/library_management.json))
        - It will provide access token and refresh token for superuser.
        - use this end point```/authorize-user``` and provide necessary info(*set is_library_admin=True) (Example: [Here](Resources/API Collections/library_management.json))

- Now library admin can signin using ```/authorize-user``` and can do library administrative work using ```access_token``` got from response (Example: [Here](Resources/API Collections/library_management.json))

##### Sign up/Sign In for a Member
- using ```'/email-signup'``` api member can signup
- S/he will be able to sign in and get token once authorized by Library Admin/Super User (using```/authorize-user``` and provide necessary info(*set is_library_admin=False))

##### Signup for Author
- To create Author an user must be created this regards. Can be done using ```'/email-signup'```
- Using ```/create-author``` library admin can register an author.
- Author can be updated and deleted by library admin using ```/update-author``` and ```/delete-author``` respectively

##### Book creation
- Two steps needed to create book
    1. ```/create-category``` - Book Category Creation
    2. ```/create-book``` - Book Creation
- Book can be updated and deleted by library admin using ```/update-book``` and ```/delete-book``` respectively

##### Book Loan Creation


##### Library Admin functionalities
- ```/create-category``` - Book Category Creation
- ```/create-author``` - Author Creation
- ```/create-book``` - Book Creation

##### Member functionalities