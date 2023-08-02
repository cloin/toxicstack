# ToxicStack

ToxicStack is a small demo stack. It contains a demo app (httpbin) and a proxy (toxiproxy) that can be configured to simulate a number of network conditions.

Httpbin is a simple HTTP request/response service, often used as a test or debugging tool, that accepts requests and, in turn, sends back responses with specified parameters, making it a valuable tool for testing client HTTP connections. 

On the other hand, Toxiproxy is a TCP proxy designed to simulate network and system conditions for automated tests, enabling developers to test how their application handles various network failures and slowdowns.

This podman compose sets up both containers and exposes required ports to proxy clients through toxiproxy to httpbin allowing you to create, test and monitor network conditions affecting your app.

# Setup

**1. Install podman and podman-compose**

**2. Clone the repo and cd into it the directory**

**3. Start the stack with:**
```bash
podman-compose up -d
```

# Usage

**1. Create the proxy if it doesn't exist**

```bash
curl -X POST http://localhost:8474/proxies -d '{
    "name": "httpbin_proxy",
    "listen": "[::]:8001",
    "upstream": "httpbin:80"
}'
```

**2. Add a latency toxic**

```bash
curl -X POST http://localhost:8474/proxies/httpbin_proxy/toxics -d '{
    "name": "latency_toxic",
    "type": "latency",
    "stream": "downstream",
    "attributes": {"latency": 5000}
}'
```

**3. Delete the toxi**


```bash
curl -X DELETE http://localhost:8474/proxies/httpbin_proxy/toxics/latency_toxic
```

**4. List proxies**

To list all the proxies in Toxiproxy, you can use the following command:

```bash
curl http://localhost:8474/proxies
```

The above command will return a JSON object with all the proxies currently set up in Toxiproxy.

**5. Test client request**

To test your httpbin proxy, you would connect to it through the port you set up in Toxiproxy (in this case, port 8001). For example:

```bash
curl http://localhost:8001/get
```

This will make a GET request to the `httpbin` service through the `toxiproxy` and the response should be delayed by the amount of latency you've configured in Toxiproxy.
