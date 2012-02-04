#!/bin/sh

case "$1" in
	web) 
		nohup ./webserver.py & 
		echo $! > ~/.lerner/webserver.pid;;
	pubsub) 
		nohup ./notify_server.py & 
		echo $! > ~/.lerner/pubsubserver.pid;;
	*)
		$0 pubsub 
		$0 web ;;
esac
