import time
import speedtest
from prometheus_client import start_http_server, Gauge

# Define Prometheus metrics
download_speed = Gauge('internet_download_speed', 'Download speed in Mbps')
upload_speed = Gauge('internet_upload_speed', 'Upload speed in Mbps')
ping = Gauge('internet_ping', 'Ping in milliseconds')


def run_speed_test(st):
    try:
        # Run speedtest-cli and capture the output
        st.download()
        st.upload()

        # Extract metrics
        download_speed.set(st.results.dict()['download'] / 1_000_000)  # Convert from bps to Mbps
        upload_speed.set(st.results.dict()['upload'] / 1_000_000)  # Convert from bps to Mbps
        ping.set(st.results.dict()['ping'])

        print("Download: ", download_speed._value.get(), "Mbps")
        print("Upload: ", upload_speed._value.get(), "Mbps")
        print("Ping: ", ping._value.get(), "ms")

    except Exception as e:
        print(f"Error running speed test: {e}")


if __name__ == '__main__':
    # Start Prometheus client server on port 8000
    start_http_server(8085)
    print("Prometheus exporter started on port 8085...")

    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    threads = None
    # If you want to use a single threaded test
    # threads = 1

    s = speedtest.Speedtest(secure=True)
    s.get_servers(servers)
    s.get_best_server()

    # Run speed test periodically
    while True:
        run_speed_test(s)
        time.sleep(300)  # Run every 5 minutes
