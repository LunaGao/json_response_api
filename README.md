# json_response

```shell
pip3 freeze > requirements.txt  # Python3
pip freeze > requirements.txt  # Python2 / venv
```

# debug
```shell
uvicorn main:app --reload
```

# aliyun
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
gunicorn main:app -D -w 4 -b 127.0.0.1:8765 -k uvicorn.workers.UvicornWorker
gunicorn -w 4 -b 127.0.0.1:8765 -D main:app
gunicorn -w 4 -b 127.0.0.1:8765 main:app
deactivate

kill $(lsof -i:8765|awk '{if(NR==2)print $2}')