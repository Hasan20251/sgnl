#!/usr/bin/env python3
"""
Code Profiling Tool for SGNL Backend

Usage:
    python profile_code.py --function deep_scan
    python profile_code.py --url http://example.com
    python profile_code.py --all
"""

import time
import cProfile
import pstats
import io
import sys
from functools import wraps
from typing import Callable, Any, Dict
import argparse


def profile_function(func: Callable) -> Callable:
    """Decorator to profile a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        pr.disable()

        # Print results
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(30)  # Top 30 functions

        print(f"\n{'='*80}")
        print(f"Function: {func.__name__}")
        print(f"Execution Time: {end_time - start_time:.4f}s")
        print(f"{'='*80}")
        print(s.getvalue())

        return result

    return wrapper


def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure and print execution time."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print(f"[TIMING] {func.__name__}: {end_time - start_time:.4f}s")

        return result

    return wrapper


class PerformanceProfiler:
    """Simple performance profiler for code analysis."""

    def __init__(self):
        self.timings: Dict[str, list] = {}

    def time_function(self, name: str):
        """Context manager to time a function execution."""

        class Timer:
            def __init__(self, profiler, name):
                self.profiler = profiler
                self.name = name
                self.start_time = None

            def __enter__(self):
                self.start_time = time.time()
                return self

            def __exit__(self, *args):
                elapsed = time.time() - (self.start_time or 0)
                if self.name not in self.profiler.timings:
                    self.profiler.timings[self.name] = []
                self.profiler.timings[self.name].append(elapsed)

        return Timer(self, name)

    def print_summary(self):
        """Print timing summary."""
        print(f"\n{'='*80}")
        print("PERFORMANCE TIMING SUMMARY")
        print(f"{'='*80}")
        print(f"{'Operation':<50} {'Calls':<10} {'Total':<12} {'Avg':<12} {'Max':<12}")
        print(f"{'-'*80}")

        for name, times in sorted(self.timings.items()):
            total = sum(times)
            avg = total / len(times)
            max_time = max(times)
            print(f"{name:<50} {len(times):<10} {total:<12.4f} {avg:<12.4f} {max_time:<12.4f}")

        print(f"{'='*80}\n")


# Example usage with actual code
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Profiling Tool")
    parser.add_argument("--function", help="Function to profile")
    parser.add_argument("--url", help="URL to test (for extraction)")
    parser.add_argument("--all", action="store_true", help="Profile all critical functions")

    args = parser.parse_args()

    profiler = PerformanceProfiler()

    # Example: Profile HTML parsing
    @timing_decorator
    def test_html_parsing():
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Main Heading</h1>
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
                <div>Content div</div>
                <a href="https://example.com">Link</a>
            </body>
        </html>
        """ * 100

        # Simple string operations as proxy for parsing
        title_count = html.count("<title>")
        paragraph_count = html.count("<p>")
        link_count = html.count("<a")

        return title_count + paragraph_count + link_count

    # Example: Database query simulation
    @timing_decorator
    def test_query_simulation():
        """Simulate database query latency."""
        time.sleep(0.01)  # Simulate 10ms query
        return [1, 2, 3, 4, 5]

    # Example: Regex matching
    @timing_decorator
    def test_regex_matching():
        import re

        affiliate_patterns = [
            r"amzn\.to",
            r"shareasale",
            r"clickbank",
            r"cj\.com",
            r"affiliate",
        ]

        text = "This is a test page with amzn.to link and affiliate content" * 1000

        count = 0
        for pattern in affiliate_patterns:
            if re.search(pattern, text):
                count += 1

        return count

    # Example: List operations
    @timing_decorator
    def test_list_operations():
        data = [i for i in range(10000)]

        # Simulate rate limiter cleanup
        now = time.time()
        old_data = [i for i in data if now - i < 60]

        return len(old_data)

    # Run profiling
    print("Running performance profile...\n")

    test_html_parsing()
    test_query_simulation()
    test_regex_matching()
    test_list_operations()

    profiler.print_summary()
