# FastAPI
## Execute
```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```
We have a database example file discord.sql


## Document
Once you execute FastAPI by above command, you can watch document at http://127.0.0.1:8000/docs
![image](https://user-images.githubusercontent.com/72553977/218235383-9bb4e4ea-b266-4997-9894-b26aef493a28.png)
