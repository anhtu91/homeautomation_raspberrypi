#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('admin1', 'admin1')
parameters = pika.ConnectionParameters('192.168.1.2',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()