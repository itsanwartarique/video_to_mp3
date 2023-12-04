import pika,sys,os,json
from convert.to_mp3 import to_mp3


def main():
    # rabbitmq connection
    url = "amqp://admin:admin@localhost:5672"
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        body = json.loads(body)
        username = body["username"]
        video_id = body["video_id"]
        print(username,video_id)
        mp3_id,err = to_mp3(video_id)

        if not err:
            channel.queue_declare("audio")
            
            message = {
                "audio_id" : mp3_id,
                "username " : username
            }
            try:
                channel.basic_publish(
                exchange="",
                routing_key="audio",
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
            except Exception as err:
                print(err)
                return "internal server error", 500
        else:
            print(err)


    channel.basic_consume(
        queue="video", on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)