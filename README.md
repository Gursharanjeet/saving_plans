# saving_plans
# Steps for using the project
### Please create a virtual env using this package of python 
  https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.
### Once you have created the env, now activate it using:
  source env_name/bin/activate
### Then install the all the requirements using this: 
  pip install -r requirment.txt
### Once all the requirements are installed, please migrate your model to db in this project I have used SQLite3 as it is the default db for the python, you can migrate the model using.
  python manage.py migrate
### Once the model is migrated successfully run the project using this:
  python manage.py runserver
### This project has this URL working please use this documentation for the references
   https://documenter.getpostman.com/view/12176211/UzBqq6Jk
