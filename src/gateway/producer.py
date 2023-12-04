import pika,json

def publish(username,video_id):    
    # conneciton
    url = "amqp://admin:admin@localhost:5672"
    connection = pika.BlockingConnection(pika.URLParameters(url))
    # channel
    channel = connection.channel()

    channel.queue_declare(queue="video")
    
    message = {
        "video_id": video_id,
        "username": username,
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        return "internal server error", 500