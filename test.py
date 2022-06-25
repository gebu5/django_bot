import requests
import time



time_p = time.time()
#r = requests.post('https://ticket-site-app.herokuapp.com/api/event_info/', json={'event_id':4})
print(time.time() - time_p)

r = requests.post('http://127.0.0.1:8000/api/event_info/', json={'event_id':4})

print(r.json())