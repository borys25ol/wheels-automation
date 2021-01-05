Wheels Google Spreadsheet API
====================

Local install
-------------

Setup and activate a python3 virtualenv via your preferred method. e.g. and install production requirements:


    $ make ve
  
For remove virtualenv:


    $ make clean

Local run
-------------
Copy Google credentials json file to `credentials` folder and name it `google_creds.json`.

Export path to Environment Variables:


    $ export PYTHONPATH='/path-to-project-dir'
 
Start debug server:


    $ python wsgi.py
    OR:
    $ make runserver

    
If everything is fine, check this endpoint:

    $ curl -X "GET" http://host:port/api/healh-check

Expected result:

```
{
  "success": true
}
```
