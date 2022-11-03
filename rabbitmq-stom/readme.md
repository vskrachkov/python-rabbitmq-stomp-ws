### Installed plugins:
* rabbitmq_prometheus
* rabbitmq_web_stomp
* rabbitmq_stomp
* rabbitmq_management
* rabbitmq_web_dispatch
* rabbitmq_management_agent

### rabbit_stomp 
default user: `guest/guest`

### Ports
| Service                  | Exposed port | Internal port |
|--------------------------|--------------|---------------|
| Management plugin        | 15672        | 15672         |
| STOMP TCP listener       | 61613        | 61613         |
| rabbit_web_stomp         | 15674        | 15674         |
| AMQP TCP listener        | 5672         | 5672          |
| Prometheus metrics: HTTP | -            | 15692         |
