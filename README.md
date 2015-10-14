#nyctax#
Simple NYC tax calculator

##Installation##
1. git clone
2. Create environment
  * `virtualenv venv`
3. Modify config.py if necessary
4. Activate environment
  * `. venv/bin/activate`
5. Install required libraries
  * `pip install -r requirements.txt`
6. Create DB
  * `python db_create.py`
7. Populate DB (or use admin panel once running)
  * `python db_populate.py`
8. Run
  * `python run.py`