FROM confluentinc/cp-kafka-connect:5.5.4

WORKDIR /connect

ENV CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components"

COPY mongodb-kafka-connect-mongodb-1.5.0.zip .

RUN  confluent-hub install --no-prompt confluentinc/kafka-connect-datagen:latest
RUN apt-get update &&\
    apt-get install unzip &&\
    unzip -d ./mongodb-kafka ./mongodb-kafka-connect-mongodb-1.5.0.zip &&\
    find ./mongodb-kafka -maxdepth 1 -type d ! -wholename "./mongodb-kafka" -exec mv {} /usr/share/confluent-hub-components/kafka-connect-mongodb \;
