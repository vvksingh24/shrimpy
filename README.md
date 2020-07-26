# Shrimpy

Get exchange rate for crypto's on different exchanges

## Getting Started

clone the repo

```
git clone https://github.com/vvksingh24/shrimpy.git
```

### Prerequisites

python3+

### Installing

run the setup file to install the requirement's

For Ubuntu based systems:
```
bash setup.sh
```
For Mac:
zsh (Mac Catalina) and bash (Earlier macOS)
```
zsh setup_for_mac.sh
```

## Running the services

start redis-server

For ubuntu:
```
sudo service redis-server status
```
for mac:
```
brew services start redis
```
Activate virtual environment

```
source virtualenvname/bin/activate
```
check out to project directory:
```
cd project_dir
```
start celery-worker and celery-beat
```
celery -A coinswitch worker -l info

celery -A coinswitch beat -l info
```
start the server
```
python manage.py runserver
```
wait for around 2 min till system get's synced

## Usage
Hit the api:

```
http://localhost:8000/exchange-rate?exchange=KUCOIN&fromCurrency=btc&toCurrency=usdt
```
To check response time
 
--> check response headers `X-total-time-ms` 

--> check time in postman or in network tab of browser

--> uncomment this code in `trader/middleware.py

Note: this works only in browser postman will show parsing error
```
# if isinstance(response, Response):
        #     response.data['time'] = f'{duration * 1000}ms'
        #     response._is_rendered = False
        #     response.render()
```
 

## Authors

* **Vivek Singh** 
