#!/bin/sh
set -e

supervisord -c /beacon/supervisord.conf

exec nginx -c /beacon/nginx.conf -g "daemon off;"