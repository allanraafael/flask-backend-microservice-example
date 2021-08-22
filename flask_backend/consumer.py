import pika, json

from config import CLOUDAMQP_URL

from app import Product, db


params = pika.URLParameters(CLOUDAMQP_URL)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='flask')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print("[x] Received in flask " + str(data))

    if properties.content_type == 'product_created':
        product = Product(
            id=data['id'], title=data['title'], image=data['image'])

        db.session.add(product)
        db.session.commit()
        print("product created in flask")

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print("product updated in flask")


    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print("product deleted in flask")


channel.basic_consume(
    queue='flask', on_message_callback=callback, auto_ack=True)

print('[*] Waiting for messages in flask:')
channel.start_consuming()
channel.close()
