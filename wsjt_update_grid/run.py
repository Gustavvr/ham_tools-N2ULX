#!/usr/bin/python3

## https://github.com/n4af/TR4W/wiki/WSJT-X-UDP-Interface-API

import gps
## https://gpsd.gitlab.io/gpsd/gpsd_json.html

import maidenhead as mh
import socket
import sys

 
# Listen on port 2947 (gpsd) of localhost
#session = gps.gps("localhost", "2947")
session = gps.gps()

session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
 
while True:
    try:
        report = session.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and  hasattr(report, 'lon'):
                grid=mh.to_maiden(report.lat, report.lon, precision = 2 )
                print(grid, file=sys.stderr)
                break
                
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("GPSD has terminated", file=sys.stderr)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
#server_address = ('localhost', 2242)
server_address = ('localhost', 2237)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

message = "{\"type\":\"STATION.SET_GRID\",\"value\":\"" + grid + "\"}"

print('\nwaiting to receive message', file=sys.stderr)
data, address = sock.recvfrom(4096)

print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
print(data.strip(), file=sys.stderr)

if data:
  sent = sock.sendto(message.encode('utf-8'), address)
  print('sent %s bytes back to %s' % (sent, address), file=sys.stderr)

print('\nwaiting to receive confirmation', file=sys.stderr)
data, address = sock.recvfrom(4096)

print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
print(data, file=sys.stderr)
