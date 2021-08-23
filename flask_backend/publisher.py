import pika, json

from config import CLOUDAMQP_URL


params = pika.URLParameters(CLOUDAMQP_URL)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    data = json.dumps(body)
    channel.basic_publish(
        exchange='', routing_key='django', properties=properties, body=data)
    print("[x] Sent message in flask " + str(data))
