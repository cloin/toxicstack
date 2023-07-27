from datadog_checks.base import AgentCheck
import requests
import time

class ResponseTimeCheck(AgentCheck):
    def check(self, instance):
        start_time = time.time()
        response = requests.get('http://localhost:8001/get', stream=True)
        end_time = time.time()

        response_time = end_time - start_time
        self.gauge('toxicstack.response_time', response_time)

        # Calculate connection close time
        start_close_time = time.time()
        response.close()
        end_close_time = time.time()

        close_time = end_close_time - start_close_time
        self.gauge('toxicstack.close_time', close_time)
