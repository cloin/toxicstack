# ToxicStack for Datadog

This directory contains the necessary configuration files and scripts to set up custom Datadog monitoring for the ToxicStack application.

## Directory Structure

- `checks.d/`: Contains custom Python scripts for Datadog's Agent to execute and collect metrics.
    - `toxicstack.py`: This is the custom check script for the ToxicStack application. It calculates the response time from the ToxicStack application's `/get` endpoint.
- `conf.d/`: Contains configuration data for the custom check scripts.
    - `toxicstack.d/conf.yaml`: This file provides the configuration for the custom check script.

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
