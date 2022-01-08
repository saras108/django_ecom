# Simple E-commerce web application
This project is a smiple web application using python's framework django. Only the logged in user can place the order of the product.

There are 2 groups of the user, Admin and Customer.
- Admin can manage the backend portion of the application like :
1. Add tags
2. Add Products 
3. Can update the status (pending , Delivered, Out of Stoke) of the orederd product
4. Can view the orders of individual costumer as well as all costumers.

-While Customer can place the order and delete and view the details of placed orders by self.

##Installation
To run this code you would need:

## Installation

To run this code you would need:

1. Download/ Clone the project

```git
  git clone https://github.com/saras108/django_ecom
```

2. Create a virtual environment

```python3
  python3 -m venv env
```

3. Activate the environment
```
  source env/bin/activate (for linux)
  .\env\Scripts\activate (for window)
```

4. Install the required packages

```python3
  pip3 install -r requirements.txt
``` 

5. To run migrations.
```
  python manage.py makemigrations
  python manage.py migrate
``` 

5. To create super user run.
```
python manage.py createsuperuser
```
After running this command it will ask for username, password.


6. python manage.py runserver
```python3
python manage.py runserver
```

To log in as a admin:
 ```
 localhost:8000/admin/
 ```
Enter the credencials which you have entered while creating the superuser.

After logged in as a Admin, do the following:


To Register as customer:
 ```
 localhost:8000/register/
 ```

To login as customer:
 ```
 localhost:8000/login/
 ```
Enter the credencials which you have entered while registering.

### THANK YOU :hugs: :hugs:
