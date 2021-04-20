# AudioServe

A pseudo database for audiofiles. As CRUD capabilities for songs, poscasts and audiobooks. This project is an assignment by Filed.

### Setup

```
cd AudioServe
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
python3 manage.py makemigrations api
python3 manage.py migrate
python3 manage.py runserver
```

### Usage

1. All POST data should be entered as dictionary in the request body. For example, as form-data in Postman.
2. All Urls must end with /, or you might get 301 redirect.
3. The participants field must a comma separated string. For example, `adam, bob, carl, dennis`. This is parsed and saved as `json` in the database.
4. For update, only the field that needs to be changed may be entered. Re-entering all the key-value pairs is not necessary.
**Create: ** `localhost:8000/create/audioType/`
**Read: ** `localhost:8000/read/audioType/` or `localhost:8000/read/song/2/`
**Update: ** `localhost:8000/update/podcast/2/`
**Delete: ** `localhost:8000/delete/audiobook/2/`

### Thank you and have fun.