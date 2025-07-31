import json
import time
from azure.eventhub import EventHubProducerClient, EventData

CONNECTION_STR = "Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<key-name>;SharedAccessKey=<key>"
EVENTHUB_NAME = "trip-events"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME
)

print("🚖 Starting to send simulated trip events... Press Ctrl+C to stop.")

try:
    while True:
        trip_event = {
            "vendorID": "Vendor1",
            "tripDistance": 0.5,
            "passengerCount": 5,
            "paymentType": "2"
        }
        event_data = EventData(json.dumps(trip_event))
        producer.send_batch([event_data])
        print(f"Sent: {trip_event}")
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped sending events")
