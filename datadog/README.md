# ToxicStack for Datadog

This directory contains the necessary configuration files and scripts to set up custom Datadog monitoring for the ToxicStack application.

## Directory Structure

- `checks.d/`: Contains custom Python scripts for Datadog's Agent to execute and collect metrics.
    - `toxicstack.py`: This is the custom check script for the ToxicStack application. It calculates the response time and close time from the ToxicStack application's `/get` endpoint.
- `conf.d/`: Contains configuration data for the custom check scripts.
    - `toxicstack.d/conf.yaml`: This file provides the configuration for the custom check script.
 
## Exposed metrics

The `toxicstack.py` script is sending two metrics to Datadog:

1. `toxicstack.response_time`: This metric measures the time it takes to receive a response from the service when making a GET request. The time is measured in seconds. The lower the response time, the faster the service is responding. 

    Toxiproxy's "latency" toxic can be used to increase this response time. The "latency" toxic adds a delay to all data going through the proxy, simulating a high-latency network connection. By increasing the latency, you can observe how the `toxicstack.response_time` metric increases in response.

    Here's an example of how you might configure a latency toxic in Toxiproxy:
    ```shell
    curl -X POST http://localhost:8474/proxies/httpbin_proxy/toxics \
      -d '{
            "type": "latency",
            "name": "latency_toxic",
            "attributes": {
                "latency": 3000,
                "jitter": 100
            }
          }'
    ```
    This command adds a latency toxic to the "httpbin_proxy" proxy, introducing a delay of 3000 milliseconds (or 3 seconds) to all traffic passing through the proxy. The "jitter" attribute adds a random variation to the latency, which can make the network delay more realistic.

2. `toxicstack.close_time`: This metric measures the time it takes to close the connection after receiving the response from the service. The time is measured in seconds. The lower the close time, the faster the service is able to close the connection.

    Toxiproxy's "slow_close" toxic can be used to increase this close time. The "slow_close" toxic delays the closing of the connection, simulating a service that is slow to acknowledge the completion of a request.

    Here's an example of how you might configure a slow_close toxic in Toxiproxy:
    ```shell
    curl -X POST http://localhost:8474/proxies/httpbin_proxy/toxics \
      -d '{
            "type": "slow_close",
            "name": "slow_close_toxic",
            "attributes": {
                "delay": 3000
            }
          }'
    ```
    This command adds a slow_close toxic to the "httpbin_proxy" proxy, introducing a delay of 3000 milliseconds (or 3 seconds) to the closing of the connection. As a result, the `toxicstack.close_time` metric should increase.

Both of these metrics can be useful for monitoring the performance of your services under different network conditions. For example, you might want to see how your service performs when network latency is high, or when connections are slow to close. By adjusting the toxics in Toxiproxy, you can simulate these conditions and observe their impact on your service's performance.

## Setup Instructions

Follow these steps to set up Datadog monitoring for ToxicStack:

1. **Clone the repository**: Clone this repository to a location accessible by the Datadog agent.

    ```
    git clone <repo_url>
    cd toxicstack/datadog
    ```

2. **Install Datadog Agent**: If not already installed, [follow these instructions](https://docs.datadoghq.com/agent/basic_agent_usage/?tab=agentv6v7) to install and configure the Datadog agent.

3. **Copy custom check script and configuration files**: Copy the `toxicstack.py` script to the `checks.d/` directory in the Datadog Agent's configuration directory (usually `/etc/datadog-agent/`). Also, copy the `toxicstack.d/` directory to the `conf.d/` directory in the Datadog Agent's configuration directory.

    ```
    sudo cp checks.d/toxicstack.py /etc/datadog-agent/checks.d/
    sudo cp -r conf.d/toxicstack.d /etc/datadog-agent/conf.d/
    ```

4. **Restart the Datadog Agent**: To load the new custom check, restart the Datadog Agent.

    ```
    sudo service datadog-agent restart
    ```

    For systems using systemd:

    ```
    sudo systemctl restart datadog-agent
    ```

5. **Verify the check is running**: Run the `status` command to verify the check is running without issues.

    ```
    sudo datadog-agent status | grep toxic
    ```

    Look for `toxicstack` under the `Running Checks` section.

6. **View your metrics**: Log in to your Datadog dashboard, navigate to the "Metrics" section, and search for the `toxicstack.response_time` metric. It may take a few minutes for the metrics to appear.

---

Remember to replace `<repo_url>` with the actual URL of your git repository. Also, if the Datadog Agent configuration directory is located somewhere else on your system, adjust the paths in the instructions accordingly.
