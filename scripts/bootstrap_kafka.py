# -*- coding: utf-8 -*-
from confluent_kafka.admin import AdminClient, NewTopic
import json
topics = ['agent-broadcast', 'agent-collect']
new_topics = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in topics]
import sys
# a = AdminClient({'bootstrap.servers': 'localhost:9092'})

# # Note: In a multi-cluster production scenario, it is more typical to use a replication_factor of 3 for durability.

# # Call create_topics to asynchronously create topics. A dict
# # of <topic,future> is returned.
# fs = a.delete_topics(topics)
# for topic, f in fs.items():
#     try:
#         res = f.result()  # The result itself is None
#         print(f'Topic {topic} deleted: {res}')
#     except Exception as e:
#         print('Failed to delete topic {}: {}'.format(topic, e))

# print('==============')
# import time
# time.sleep(2)


# fs = a.create_topics(new_topics)

# # Wait for each operation to finish.
# for topic, f in fs.items():
#     try:
#         res = f.result()  # The result itself is None
#         print(f'Topic {topic} created: {res}')
#     except Exception as e:
#         print('Failed to create topic {}: {}'.format(topic, e))



print("======")
from salver.common.facts import all_facts

def resolve_type(pydantic_type):
        if pydantic_type == "integer":
                return "int"
        return pydantic_type

def get_facts_avro_mapping():
        for fact in all_facts.values():
                schema = fact.schema()
                fields = [{"name": p_name, "type": resolve_type(p_value["type"])} for p_name, p_value in schema["properties"].items()]
                fields.append({"name": "__fact_type__", "type": "string", "default": schema["title"]})
                yield {
                        "name": schema["title"],
                        "type": "record",
                        "fields": fields
                }


def pydantic_to_avro(pydantic_model):
        pydantic_schema = pydantic_model.schema()

        properties = []

        for p_name, p_value in pydantic_schema["properties"].items():
                p_type = p_value["type"]
                if p_type == "array":
                        if "$ref" in p_value["items"]:
                                if "BaseFact" not in p_value["items"]["$ref"]:
                                        print(f"UNSUPPORTED FACT {p_name}: {p_value}")
                                        sys.exit(1)
                                items = list(get_facts_avro_mapping())

                        else:
                                items = resolve_type(p_value["items"]["type"])
                        
                        new_p_type = {
                                        "type": "array",
                                        "items": items
                                }


                else:
                        new_p_type = resolve_type(p_value["type"])
                properties.append({
                        "name": p_name,
                        "type": new_p_type
                })

        title = pydantic_schema["title"]
        return json.dumps({
            "namespace": f"salver.{title}",
            "name": title,
            "type": "record",
            "fields": properties
        })


from confluent_kafka.schema_registry import SchemaRegistryClient



conf = {
    'url': 'http://127.0.0.1:8081',
}
sr = SchemaRegistryClient(conf)

for subject in sr.get_subjects():
    print('RM subject', subject)
    sr.delete_subject(subject)



from confluent_kafka.schema_registry import Schema
from salver.common.models.collect import CollectRequest


a = pydantic_to_avro(CollectRequest)
s = Schema(
        schema_str=a,
        schema_type="AVRO"
)
res = sr.register_schema("agent-collect-value", s)
res = sr.register_schema("agent-broadcast-value", s)

# for fact in all_facts.values():
#         pydantic_to_avro(fact)