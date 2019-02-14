#### This directory will host all the code focused on the development of the website.  
The website will be split into different fragments focused on the project  
and any research findings discovered.  

#### Django Documentation
https://docs.djangoproject.com/en/2.1/intro/tutorial02/  
The above tutorial document explains the concept of migrations and database access very well.

---

Important Django Management Information:

1. Change your models (in models.py).  
2. Run python manage.py makemigrations to create migrations for those changes.  
3. Run python manage.py migrate to apply those changes to the database.

https://docs.djangoproject.com/en/2.1/intro/tutorial03/  
The above tutorial document explains ths concept of templates and template/view communication and data passing.  

---
###### Keyboard Commands
> f5 = refresh
> ctrl + f5 = refresh with cache removal

###### Gunicorn / Django / Nginx / Postgresql Commands

> Remember to start your virtual environment before initiating these commands.  

**Gunicorn**

- systemctl start gunicorn  
- systemctl enable gunicorn  
- systemctl status gunicorn  

- systemctl daemon-reload  
- systemctl restart gunicorn  

**Check Gunicorn logs for errors**  

- journalctl -u gunicorn

**Nginx**

**Postgresql**

- systemctl status postgresql
- systemctl start postgresql
- systemctl enable postgresql
