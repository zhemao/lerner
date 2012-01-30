# Notistream

Notistream is based around the concept of [webhooks](http://wiki.webhooks.org), 
push notifications sent via HTTP POST requests. Webhooks are great if you have 
a server that can accept POST requests, but what if you want to receive push 
notifications on a phone or a computer on a wifi connection. To receive push 
notifications under there conditions, you need to go beyond HTTP and use a 
protocol that supports persistent connections. 

Notistream achieves this using the Redis Pub/Sub protocol. A server, 
reimplementing Redis Pub/Sub, allows clients to open persistent connections 
and subscribe to channels. A webserver receives webhooks via POST requests 
and then publishes the information to the Pub/Sub server. Connected clients 
will then see the notification on their desktop/phone/whatever.

# Installing and Running the Client

To install the client, just do `python setup.py install`. 

The command to run the client is `notistream`. The first time you run it,
the program will ask you to enter info for a configuration file.

It will ask you for host, port, and channels. Host is the hostname of the 
Pub/Sub server. Port is its port (defaulting to Redis's default port of 6379).
Channels is a comma-separated list of the channels to which you would like to
subscribe.

# Posting a notification

To send a webhook notification, make a post request to the root url of the 
webserver. The parameters of the request should be "channel", which would be
the channel to which the message will be sent, and "message", which would be
the body of the message. For instance, to send the message "hello" to channel1, 
you could do

	curl -d "message=hello&channel=channel1" http://yourserver.com/

# Running the server

Change directory into the "server" directory. To install all dependencies, run
	
	pip install -r requirements.txt

To run the server, run the startserver.sh script.

If you only want to start the webserver, type

	./startserver.sh web

If you only want to start the pub/sub server, type

	./startserver.sh pubsub

To start both servers, run the script with no arguments.


