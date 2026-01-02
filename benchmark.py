#!/usr/bin/env python3
"""
Performance Benchmarking Script for SGNL Backend

Usage:
    python benchmark.py --workers 1 --concurrent 10 --duration 30
    python benchmark.py --url http://localhost:8000/health
    python benchmark.py --all-endpoints
"""

import asyncio
import time
import httpx
import statistics
from typing import List, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import argparse
import json


@dataclass
class BenchmarkResult:
    endpoint: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_time: float
    avg_latency: float
    min_latency: float
    max_latency: float
    p50_latency: float
    p95_latency: float
    p99_latency: float
    requests_per_second: float
    errors: List[str]


class PerformanceBenchmarker:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 60.0):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def benchmark_endpoint(
        self,
        endpoint: str,
        method: str = "GET",
        payload: Dict[str, Any] = None,
        concurrent: int = 10,
        duration: int = 30
    ) -> BenchmarkResult:
        """
        Benchmark a single endpoint.

        Args:
            endpoint: API endpoint path
            method: HTTP method
            payload: Request body for POST/PUT
            concurrent: Number of concurrent requests
            duration: Test duration in seconds
        """
        url = f"{self.base_url}{endpoint}"
        latencies = []
        errors = []
        start_time = time.time()
        total_requests = 0
        successful_requests = 0
        failed_requests = 0

        print(f"\n{'='*70}")
        print(f"Benchmarking: {method} {url}")
        print(f"Concurrency: {concurrent} | Duration: {duration}s")
        print(f"{'='*70}\n")

        async def make_request() -> float:
            """Make a single request and return latency."""
            nonlocal total_requests, successful_requests, failed_requests

            try:
                req_start = time.time()
                if method == "GET":
                    response = await self.client.get(url)
                elif method == "POST":
                    if payload:
                        response = await self.client.post(url, json=payload)
                    else:
                        response = await self.client.post(url)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                req_latency = time.time() - req_start
                total_requests += 1

                if response.status_code < 400:
                    successful_requests += 1
                    return req_latency
                else:
                    failed_requests += 1
                    errors.append(f"HTTP {response.status_code}")
                    return req_latency

            except Exception as e:
                failed_requests += 1
                total_requests += 1
                errors.append(f"Exception: {str(e)[:50]}")
                return 0.0

        # Run benchmark for duration
        semaphore = asyncio.Semaphore(concurrent)

        async def request_worker():
            """Worker that makes requests until duration expires."""
            while time.time() - start_time < duration:
                async with semaphore:
                    latency = await make_request()
                    if latency > 0:
                        latencies.append(latency)

        # Create workers
        workers = [asyncio.create_task(request_worker()) for _ in range(concurrent)]
        await asyncio.gather(*workers)

        total_time = time.time() - start_time

        # Calculate statistics
        if latencies:
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            sorted_latencies = sorted(latencies)
            p50_latency = sorted_latencies[int(len(latencies) * 0.5)]
            p95_latency = sorted_latencies[int(len(latencies) * 0.95)]
            p99_latency = sorted_latencies[int(len(latencies) * 0.99)]
        else:
            avg_latency = min_latency = max_latency = 0.0
            p50_latency = p95_latency = p99_latency = 0.0

        rps = total_requests / total_time if total_time > 0 else 0

        return BenchmarkResult(
            endpoint=endpoint,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            total_time=total_time,
            avg_latency=avg_latency,
            min_latency=min_latency,
            max_latency=max_latency,
            p50_latency=p50_latency,
            p95_latency=p95_latency,
            p99_latency=p99_latency,
            requests_per_second=rps,
            errors=errors[:10]  # Keep first 10 errors
        )

    def print_result(self, result: BenchmarkResult):
        """Print benchmark results in a formatted table."""
        print(f"\n{'='*70}")
        print(f"Results: {result.endpoint}")
        print(f"{'='*70}")
        print(f"Total Requests:      {result.total_requests:8}")
        print(f"Successful:          {result.successful_requests:8}")
        print(f"Failed:             {result.failed_requests:8}")
        print(f"Success Rate:        {result.successful_requests/result.total_requests*100:8.1f}%")
        print(f"\nTotal Time:          {result.total_time:8.2f}s")
        print(f"Requests/sec:        {result.requests_per_second:8.2f}")
        print(f"\nLatency (ms):")
        print(f"  Average:           {result.avg_latency*1000:8.2f}")
        print(f"  Minimum:           {result.min_latency*1000:8.2f}")
        print(f"  Maximum:           {result.max_latency*1000:8.2f}")
        print(f"  P50:               {result.p50_latency*1000:8.2f}")
        print(f"  P95:               {result.p95_latency*1000:8.2f}")
        print(f"  P99:               {result.p99_latency*1000:8.2f}")

        if result.errors:
            print(f"\nTop Errors:")
            for error in result.errors:
                print(f"  - {error}")

        print(f"{'='*70}\n")

    async def benchmark_all_endpoints(self, concurrent: int = 10, duration: int = 30):
        """Benchmark all major endpoints."""
        print(f"\n{'='*70}")
        print(f"COMPREHENSIVE PERFORMANCE BENCHMARK")
        print(f"{'='*70}")

        results = []

        # Health check
        result = await self.benchmark_endpoint("/health", "GET", concurrent=concurrent, duration=duration)
        results.append(result)

        # Extract endpoint
        result = await self.benchmark_endpoint(
            "/extract",
            "POST",
            payload={"url": "https://example.com"},
            concurrent=concurrent,
            duration=duration
        )
        results.append(result)

        # Check density
        result = await self.benchmark_endpoint(
            "/check-density",
            "POST",
            payload={
                "results": [{"url": "https://example.com", "content": "Test content" * 100}],
                "threshold": 0.45
            },
            concurrent=concurrent,
            duration=duration
        )
        results.append(result)

        # Print summary
        print(f"\n{'='*70}")
        print(f"BENCHMARK SUMMARY")
        print(f"{'='*70}")
        print(f"{'Endpoint':<30} {'RPS':<10} {'P95(ms)':<10} {'Success%':<10}")
        print(f"{'-'*70}")
        for result in results:
            print(f"{result.endpoint:<30} {result.requests_per_second:<10.2f} {result.p95_latency*1000:<10.2f} {result.successful_requests/result.total_requests*100:<10.1f}")

        return results

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


async def main():
    parser = argparse.ArgumentParser(description="SGNL Performance Benchmarking Tool")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL")
    parser.add_argument("--endpoint", help="Single endpoint to benchmark")
    parser.add_argument("--method", default="GET", help="HTTP method")
    parser.add_argument("--payload", help="JSON payload for POST requests")
    parser.add_argument("--concurrent", type=int, default=10, help="Concurrent requests")
    parser.add_argument("--duration", type=int, default=30, help="Test duration (seconds)")
    parser.add_argument("--all-endpoints", action="store_true", help="Benchmark all endpoints")

    args = parser.parse_args()

    benchmarker = PerformanceBenchmarker(base_url=args.url)

    try:
        if args.all_endpoints:
            await benchmarker.benchmark_all_endpoints(concurrent=args.concurrent, duration=args.duration)
        elif args.endpoint:
            payload = json.loads(args.payload) if args.payload else None
            result = await benchmarker.benchmark_endpoint(
                endpoint=args.endpoint,
                method=args.method,
                payload=payload,
                concurrent=args.concurrent,
                duration=args.duration
            )
            benchmarker.print_result(result)
        else:
            # Default: health check
            result = await benchmarker.benchmark_endpoint("/health", concurrent=args.concurrent, duration=args.duration)
            benchmarker.print_result(result)

    finally:
        await benchmarker.close()


if __name__ == "__main__":
    asyncio.run(main())
