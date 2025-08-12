import requests
import time
from statistics import mean
from prettytable import PrettyTable
from datetime import datetime

# List of websites to performance test
websites = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.instagram.com",
    "https://www.twitter.com",
    "https://www.linkedin.com",
    "https://www.youtube.com",
    "https://www.reddit.com",
    "https://www.tiktok.com",
    "https://www.pinterest.com",
    "https://www.whatsapp.com"
]

# Config
REQUESTS_PER_SITE = 5
TIMEOUT = 5  # seconds

def performance_test(url, runs=5):
    times = []
    errors = 0
    for _ in range(runs):
        try:
            start = time.time()
            resp = requests.get(url, timeout=TIMEOUT)
            elapsed = time.time() - start
            if resp.ok:
                times.append(elapsed)
            else:
                errors += 1
        except requests.exceptions.RequestException:
            errors += 1

    if times:
        return {
            "url": url,
            "min_time": min(times),
            "max_time": max(times),
            "avg_time": mean(times),
            "success_rate": 100 - (errors / runs * 100),
            "errors": errors
        }
    else:
        return {
            "url": url,
            "min_time": None,
            "max_time": None,
            "avg_time": None,
            "success_rate": 0,
            "errors": errors
        }

if __name__ == "__main__":
    print(f"\n🚀 Website Performance Test Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Running {REQUESTS_PER_SITE} requests per site...\n")

    results = []
    for site in websites:
        stats = performance_test(site, REQUESTS_PER_SITE)
        results.append(stats)

    # Sort by average time (fastest first)
    results.sort(key=lambda x: x["avg_time"] if x["avg_time"] is not None else float("inf"))

    # Create a nice table
    table = PrettyTable()
    table.field_names = ["Rank", "Website", "Min (s)", "Max (s)", "Avg (s)", "Success Rate (%)", "Errors"]

    for i, res in enumerate(results, start=1):
        table.add_row([
            i,
            res["url"],
            f"{res['min_time']:.3f}" if res["min_time"] else "N/A",
            f"{res['max_time']:.3f}" if res["max_time"] else "N/A",
            f"{res['avg_time']:.3f}" if res["avg_time"] else "N/A",
            f"{res['success_rate']:.1f}",
            res["errors"]
        ])

    print(table)

    # Summary
    total_errors = sum(r["errors"] for r in results)
    avg_of_avgs = mean([r["avg_time"] for r in results if r["avg_time"] is not None])

    print("\n📊 Summary Report")
    print(f"Total Sites Tested: {len(websites)}")
    print(f"Total Requests: {len(websites) * REQUESTS_PER_SITE}")
    print(f"Total Errors: {total_errors}")
    print(f"Average Response Time Across All Sites: {avg_of_avgs:.3f} seconds")
    print(f"Fastest Site: {results[0]['url']} ({results[0]['avg_time']:.3f}s avg)")
    slowest = max([r for r in results if r['avg_time'] is not None], key=lambda x: x["avg_time"])
    print(f"Slowest Site: {slowest['url']} ({slowest['avg_time']:.3f}s avg)")
