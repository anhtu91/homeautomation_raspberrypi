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

channel.queue_declare(queue='task_queue', durable=True)

for i in range(1,10): 
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message+str(i),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
print(" [x] Sent %r" % message)
connection.close()