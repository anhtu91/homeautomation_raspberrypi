#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = ['error', 'info', 'warning']

for s in routing_key:
    if(s=='error'):
        message = 'Error World!'
    elif(s=='info'):
        message = 'Info World!'
    elif(s=='warning'):
        message = 'Warning World!'
    channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
    
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()