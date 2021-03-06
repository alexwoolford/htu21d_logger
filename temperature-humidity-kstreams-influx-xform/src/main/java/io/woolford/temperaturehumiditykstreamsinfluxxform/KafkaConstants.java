package io.woolford.temperaturehumiditykstreamsinfluxxform;

public interface KafkaConstants {

    public static String KAFKA_BROKERS = "cp01.woolford.io:9092,cp02.woolford.io:9092,cp03.woolford.io:9092";
    public static String APPLICATION_ID = "kstreams-temperature-humidity-influx-xform";
    public static String SCHEMA_REGISTRY_URL = "http://cp01.woolford.io:8081";

}
