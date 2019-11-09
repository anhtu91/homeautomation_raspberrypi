#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('admin1', 'admin1')
parameters = pika.ConnectionParameters('192.168.1.2',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World! Anh Tu Nguyen')
print(" [x] Sent 'Hello World!'")
connection.close()