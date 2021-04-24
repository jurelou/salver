from confluent_kafka.admin import AdminClient, NewTopic


a = AdminClient({'bootstrap.servers': 'localhost:9092'})

new_topics = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in ["topic1", "topic2"]]
# Note: In a multi-cluster production scenario, it is more typical to use a replication_factor of 3 for durability.

# Call create_topics to asynchronously create topics. A dict
# of <topic,future> is returned.
fs = a.delete_topics(["topic1", "topic2"])
for topic, f in fs.items():
    try:
        res = f.result()  # The result itself is None
        print(f"Topic {topic} created: {res}")
    except Exception as e:
        print("Failed to rm topic {}: {}".format(topic, e))

print("==============")
import time
time.sleep(2)


fs = a.create_topics(new_topics)

# Wait for each operation to finish.
for topic, f in fs.items():
    try:
        res = f.result()  # The result itself is None
        print(f"Topic {topic} created: {res}")
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))




from confluent_kafka.schema_registry import SchemaRegistryClient


conf = {
    "url": "http://127.0.0.1:8081"
}
sr = SchemaRegistryClient(conf)

for subject in sr.get_subjects():

    print("!!subject", subject)
    sr.delete_subject(subject)