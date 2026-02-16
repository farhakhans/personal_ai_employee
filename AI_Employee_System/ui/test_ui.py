"""
Test script for the Flask UI using Flask test client.
Runs create + publish flows for Facebook and Instagram and prints results.
"""

from app import create_app

app = create_app()

with app.test_client() as c:
    print('\n-- Facebook create')
    r = c.post('/facebook/create', json={'topic':'sales','details':{'action':'closed a deal','text':'Saved 30%'}})
    print(r.status_code, r.json)

    print('\n-- Facebook publish')
    r = c.post('/facebook/publish')
    print(r.status_code, r.json)

    print('\n-- Instagram create')
    r = c.post('/instagram/create', json={'text':'Automating business tasks with AI.'})
    print(r.status_code, r.json)

    print('\n-- Instagram publish')
    r = c.post('/instagram/publish')
    print(r.status_code, r.json)

    print('\n-- Social logs')
    r = c.get('/social/logs')
    print(r.status_code)
    for k,v in (r.json or {}).items():
        print('-', k, 'entries:', len(v))
