#!/bin/sh

case "$1" in
	web) nohup ./webserver.py & ;;
	pubsub) nohup ./notify_server.py & ;;
	*) $0 pubsub; $0 web ;;
esac
