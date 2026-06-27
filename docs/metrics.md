# Benchmark Metrics

Generated from:

```bash
python3 scripts/benchmark.py
```

Benchmark context:

* Generated: `2026-06-27T09:16:16.975096+00:00`
* Target: `http://127.0.0.1:8000`
* Iterations: `5`
* Total requests: `30`
* Total benchmark duration: `108.22s`

## Summary

| Metric | Result |
| --- | ---: |
| Throughput | `0.28 requests/sec` |
| Error rate | `0.00%` |
| p50 latency | `60.83 ms` |
| p95 latency | `2307.63 ms` |
| p99 latency | `100459.07 ms` |

## Cold-Start Behavior

The p99 latency is dominated by the first real call to `POST /evaluations/{id}/evaluate`, which initializes the SentenceTransformer model inside the API container.

Observed cold-start outlier:

* Endpoint: `POST /evaluations/{id}/evaluate`
* p99 latency: `100459.07 ms`
* Error rate during benchmark: `0.00%`

## Steady-State Latency

Most non-evaluation API calls stayed under `100 ms` at p50 and p95 in this sample run.

| Endpoint | Requests | Errors | p50 latency | p95 latency |
| --- | ---: | ---: | ---: | ---: |
| `GET /evaluations/{id}/report` | 5 | 0 | `34.79 ms` | `56.91 ms` |
| `POST /evaluations` | 5 | 0 | `58.52 ms` | `372.39 ms` |
| `POST /evaluations/{id}/results` | 15 | 0 | `63.14 ms` | `90.22 ms` |

## Semantic Evaluation Latency

`POST /evaluations/{id}/evaluate` performs semantic similarity scoring and is expected to be slower than CRUD-style endpoints.

| Endpoint | Requests | Errors | p50 latency | p95 latency |
| --- | ---: | ---: | ---: | ---: |
| `POST /evaluations/{id}/evaluate` | 5 | 0 | `1360.13 ms` | `100459.07 ms` |

## Throughput

The benchmark ran sequential requests against the local Docker Compose API.

* Total requests: `30`
* Total duration: `108.22s`
* Throughput: `0.28 requests/sec`

## Error Rate

No API errors were observed during the benchmark.

* Errors: `0`
* Error rate: `0.00%`
