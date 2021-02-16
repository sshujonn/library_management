#### Why this project
- This is project is intended to create a system for role based access and distribute functionality to library admin and member user in a library.

#### How to get this project
```git clone https://github.com/sshujonn/library_management.git```

#### Install Project Prerequisites (On windows)
##### Install Python
- Check version if installed (python -V)
- Otherwise follow the steps from https://www.python.org/downloads/

##### Install pip
- Follow the steps from https://www.liquidweb.com/kb/install-pip-windows/

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
python manage.py makemigrations
```

```
python manage.py migrate
```

```
python manage.py createsuperuser
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
- using ```'/email-signup'``` api and providing necessary information (Example: [Here](Resources/API_Collections/library_management.json))
- This account need to be authorized by superadmin first which can be done by following two ways
    1. Login to admin site and go [here](http://127.0.0.1:8000/admin/users/profile/) click on the user and ```make is_authorized checked, Groups=library_admin and save```
    2. Collect Client_id and secret from [here](http://127.0.0.1:8000/o/applications). And Use ```/o/token/``` provide necessary information for superuser. (Example: [Here](Resources/API_Collections/library_management.json))
        - It will provide access token and refresh token for superuser.
        - Use this end point```/authorize-user``` and provide necessary info(*set is_library_admin=True) (Example: [Here](Resources/API_Collections/library_management.json))

- Now library admin can signin using ```/authorize-user``` and can do library administrative work using ```access_token``` got from response (Example: [Here](Resources/API_Collections/library_management.json))

##### Sign up/Sign In for a Member
- Using ```'/email-signup'``` api member can signup
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

##### Book Loan
- Book loan can be created using ```/create-book-loan``` endpoint by member.
- Admin can browse all pending book loan by using ```/browse-book-loans``` with page_no parameter where as member can only browse his own book loans.
- Admin can accept or reject book loan by using ```/update-book-loan```
- Admin can export 

##### Access Control
- ```/email-signup``` -- Open
- ```/email-signin``` -- Only signed up and authorized user
- ```/authorize-user``` -- Super admin, Library admin
- ```/browse-unauthorized-users``` -- Super admin, Library admin
- ```/create-group``` -- Super admin, Library admin
- ```/create-category``` -- Super admin, Library admin
- ```/browse-book-loans``` -- Super admin, Library admin
- ```/create-book-loan``` -- Member
- ```/update-book-loan``` -- Super admin, Library admin
- ```/export-book-loan``` -- Super admin, Library admin
- ```/browse-books``` -- All authenticated users
- ```/create-book``` -- Super admin, Library admin
- ```/update-book``` -- Super admin, Library admin
- ```/delete-book``` -- Super admin, Library admin
- ```/browse-authors``` -- All authenticated users
- ```/create-author``` -- Super admin, Library admin
- ```/update-author``` -- Super admin, Library admin
- ```/delete-author``` -- Super admin, Library admin

##### * All API Endpoints except ```/email-signup``` needs authorization token (Can be gotten from ```/o/token/``` )
##### * This project is developped using sqlite3. who uses this project can also use other database. by changing 'DATABASES' [Here](library_management/settings.py)
##### * db.sqlite3 is uploaded with dummy data for test purpose. Credentials for dummy users are given [here](Resources/API_Collections/dummy.txt)
##### * Created two testcases for API testing. To test run ```python manage.py test```