import argparse
import json
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request


DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_ITERATIONS = 5


SAMPLES = [
    (
        "Customer cannot connect to VPN after password reset.",
        "User reports VPN access failure after credential change.",
    ),
    (
        "Invoice export should include tax and discount columns.",
        "Billing export contains tax and discount fields.",
    ),
    (
        "The chatbot should escalate refund requests over $500.",
        "Refund requests above five hundred dollars are escalated.",
    ),
]


def percentile(values, percentile_value):
    if not values:
        return 0.0

    ordered = sorted(values)
    index = int(round((percentile_value / 100) * (len(ordered) - 1)))

    return ordered[index]


def call_api(method, url, payload=None):
    body = None
    headers = {}

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = request.Request(
        url,
        data=body,
        headers=headers,
        method=method,
    )

    started = time.perf_counter()

    try:
        with request.urlopen(req, timeout=120) as response:
            response_body = response.read().decode("utf-8")
            elapsed = time.perf_counter() - started

            return {
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "elapsed": elapsed,
                "body": json.loads(response_body) if response_body else {},
            }
    except error.HTTPError as exc:
        elapsed = time.perf_counter() - started

        return {
            "ok": False,
            "status": exc.code,
            "elapsed": elapsed,
            "body": {},
        }
    except Exception as exc:
        elapsed = time.perf_counter() - started

        return {
            "ok": False,
            "status": "error",
            "elapsed": elapsed,
            "body": {"error": str(exc)},
        }


def record(results, endpoint, response):
    results.append(
        {
            "endpoint": endpoint,
            "ok": response["ok"],
            "status": response["status"],
            "elapsed": response["elapsed"],
        }
    )


def run_benchmark(base_url, iterations):
    results = []
    started = time.perf_counter()

    for index in range(iterations):
        evaluation = call_api(
            "POST",
            f"{base_url}/evaluations",
            {
                "model_name": "support-assistant",
                "dataset_name": "support-regression",
                "version": f"benchmark-{index + 1}",
            },
        )
        record(results, "POST /evaluations", evaluation)

        evaluation_id = evaluation["body"].get("id")

        if not evaluation_id:
            continue

        for expected, actual in SAMPLES:
            response = call_api(
                "POST",
                f"{base_url}/evaluations/{evaluation_id}/results",
                {
                    "expected": expected,
                    "actual": actual,
                },
            )
            record(
                results,
                "POST /evaluations/{id}/results",
                response,
            )

        response = call_api(
            "POST",
            f"{base_url}/evaluations/{evaluation_id}/evaluate",
        )
        record(results, "POST /evaluations/{id}/evaluate", response)

        response = call_api(
            "GET",
            f"{base_url}/evaluations/{evaluation_id}/report",
        )
        record(results, "GET /evaluations/{id}/report", response)

    duration = time.perf_counter() - started

    return results, duration


def summarize(results, duration):
    latencies = [
        result["elapsed"] * 1000
        for result in results
    ]
    total = len(results)
    errors = len([
        result
        for result in results
        if not result["ok"]
    ])

    return {
        "total_requests": total,
        "errors": errors,
        "error_rate": (errors / total) if total else 0.0,
        "duration": duration,
        "throughput": (total / duration) if duration else 0.0,
        "p50": statistics.median(latencies) if latencies else 0.0,
        "p95": percentile(latencies, 95),
        "p99": percentile(latencies, 99),
    }


def endpoint_rows(results):
    rows = []

    for endpoint in sorted({result["endpoint"] for result in results}):
        endpoint_results = [
            result
            for result in results
            if result["endpoint"] == endpoint
        ]
        latencies = [
            result["elapsed"] * 1000
            for result in endpoint_results
        ]
        errors = len([
            result
            for result in endpoint_results
            if not result["ok"]
        ])

        rows.append(
            (
                endpoint,
                len(endpoint_results),
                errors,
                statistics.median(latencies) if latencies else 0.0,
                percentile(latencies, 95),
            )
        )

    return rows


def write_metrics(path, base_url, iterations, results, summary):
    timestamp = datetime.now(timezone.utc).isoformat()
    rows = endpoint_rows(results)

    lines = [
        "# Benchmark Metrics",
        "",
        f"- Generated: `{timestamp}`",
        f"- Target: `{base_url}`",
        f"- Iterations: `{iterations}`",
        f"- Total requests: `{summary['total_requests']}`",
        f"- Total benchmark duration: `{summary['duration']:.2f}s`",
        f"- Throughput: `{summary['throughput']:.2f} requests/sec`",
        f"- Error rate: `{summary['error_rate'] * 100:.2f}%`",
        f"- p50 latency: `{summary['p50']:.2f} ms`",
        f"- p95 latency: `{summary['p95']:.2f} ms`",
        f"- p99 latency: `{summary['p99']:.2f} ms`",
        "",
        "## Endpoint Breakdown",
        "",
        "| Endpoint | Requests | Errors | p50 latency | p95 latency |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for endpoint, requests_count, errors, p50, p95 in rows:
        lines.append(
            f"| `{endpoint}` | {requests_count} | {errors} | {p50:.2f} ms | {p95:.2f} ms |"
        )

    lines.extend(
        [
            "",
            "## Command",
            "",
            "```bash",
            "python3 scripts/benchmark.py",
            "```",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark the AI Regression Validation Framework API."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--iterations", type=int, default=DEFAULT_ITERATIONS)
    parser.add_argument(
        "--output",
        default="docs/metrics.md",
    )
    args = parser.parse_args()

    results, duration = run_benchmark(args.base_url, args.iterations)
    summary = summarize(results, duration)
    write_metrics(
        Path(args.output),
        args.base_url,
        args.iterations,
        results,
        summary,
    )

    print(json.dumps(summary, indent=2))

    if summary["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
