#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = ['error', 'info', 'warning']

for s in severity:
    if(s=='error'):
        message = 'Error World!'
    elif(s=='info'):
        message = 'Info World!'
    elif(s=='warning'):
        message = 'Warning World!'
    channel.basic_publish(exchange='direct_logs', routing_key=s, body=message)
    
print(" [x] Sent %r:%r" % (severity, message))
connection.close()