from flask import Flask, render_template
import threading
import time
from dns_check import DnsCheck
from http_check import BasicHTTPCheck
from icmp_check import ICMPCheck
from postgresql_check import PostgreSQLCheck
from music_shop_check import MusicShopCheck

app = Flask(__name__)

# Initialize scoring checks
dns_check = DnsCheck(host="172.18.1.12", team_number=1)
http_check = BasicHTTPCheck(host="172.18.0.1", timeout=5, path='/')
icmp_check = ICMPCheck(host="172.18.0.1", timeout=5)
postgresql_check = PostgreSQLCheck(
    host="192.168.1.7",
    port=5432,
    dbname="db",
    username="postgres",
    password="S3cr3tDBP@ss!"
)
music_shop_check = MusicShopCheck(
    url="http://192.168.1.5",
    username="scoreuser",
    password="Score123!"
)

# Store scoring results
scoring_results = {
    "dns": {"status": "unknown", "feedback": ""},
    "http": {"status": "unknown", "feedback": ""},
    "icmp": {"status": "unknown", "feedback": ""},
    "postgresql": {"status": "unknown", "feedback": ""},
    "music_shop": {"status": "unknown", "feedback": ""}
}

def run_scoring():
    while True:
        dns_check.execute()
        http_check.execute()
        icmp_check.execute()
        postgresql_check.execute()
        music_shop_check.execute()

        scoring_results["dns"]["status"] = dns_check.result.status
        scoring_results["dns"]["feedback"] = dns_check.result.feedback
        scoring_results["http"]["status"] = http_check.result.status
        scoring_results["http"]["feedback"] = http_check.result.feedback
        scoring_results["icmp"]["status"] = icmp_check.result.status
        scoring_results["icmp"]["feedback"] = icmp_check.result.feedback
        scoring_results["postgresql"]["status"] = postgresql_check.result.status
        scoring_results["postgresql"]["feedback"] = postgresql_check.result.feedback
        scoring_results["music_shop"]["status"] = music_shop_check.result.status
        scoring_results["music_shop"]["feedback"] = music_shop_check.result.feedback

        time.sleep(60)  # Run scoring every 60 seconds

@app.route('/')
def index():
    return render_template('index.html', scoring_results=scoring_results)

if __name__ == '__main__':
    # Start scoring thread
    scoring_thread = threading.Thread(target=run_scoring)
    scoring_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=8000)
