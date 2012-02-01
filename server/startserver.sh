#!/bin/sh

case "$1" in
	web) 
		nohup ./webserver.py & 
		echo $! > ~/.notistream/webserver.pid;;
	pubsub) 
		nohup ./notify_server.py & 
		echo $! > ~/.notistream/pubsubserver.pid;;
	*)
		$0 pubsub 
		$0 web ;;
esac
