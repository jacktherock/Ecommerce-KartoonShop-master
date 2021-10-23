
# Kartoon Shop - Ecommerce Site

Kartoon Shop is a basic Ecommerce Site created using `Django`, `HTML`, `CSS`, `Javascript`, `Jquery`, `Bootstrap`, `Fontawesome`, also used `Paypal Payment Gateway`.


## Steps to run virtual environment

 - Clone the project
```bash
  git clone https://github.com/jacktherock/Ecommerce-KartoonShop-master.git
```

 - Create a virtual environment in `KartoonShop` directory
```bash
  virtualenv venv
```

 - Now activate virtual environment
```bash
  .\venv\Scripts\activate
```

 - Now Install `requirements.txt` file
```bash
  python -m pip install -r requirements.txt
```

Know more about [Virtual Environment in Python](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)

## Steps to run Django server

 - Go to main project directory where `manage.py` locates
```bash
  cd KartoonShop
```

 - Create database
```bash
  python manage.py makemigrations
```

 - Create tables in database
```bash
  python manage.py migrate
```

 - Create Super user (Admin)
```bash
  python manage.py createsuperuser
```

 - Run Django Server
 ```bash
  python manage.py runserver
```

Now Kartoon Shop app server will run properly.



## Support
I need help on front-end and back-end.
All types of contributions will be accepted. 

# Thank You for Visiting !!
