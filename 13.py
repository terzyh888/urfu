import pandas as pd

from src.benchmark import prepare_benchmark


def get_test_data():
    return pd.DataFrame(
        [
            {
                "model": "Nova-7B",
                "task": "coding",
                "latency_ms": 1850,
                "judge_score": 0.82,
                "input_tokens": 1200,
                "output_tokens": 410,
            },
            {
                "model": "BorderModel",
                "task": "qa",
                "latency_ms": 3000,
                "judge_score": 0.80,
                "input_tokens": 1000,
                "output_tokens": 300,
            },
            {
                "model": "Atlas-Agent",
                "task": "research",
                "latency_ms": 7600,
                "judge_score": 0.88,
                "input_tokens": 3500,
                "output_tokens": 920,
            },
        ]
    )


def test_latency_schema():
    result = prepare_benchmark(get_test_data())

    assert "latency_sec" in result.columns
    assert "latency_ms" not in result.columns


def test_latency_conversion():
    result = prepare_benchmark(get_test_data())

    nova = result[result["model"] == "Nova-7B"].iloc[0]
    border = result[result["model"] == "BorderModel"].iloc[0]

    assert nova["latency_sec"] == 1.85
    assert border["latency_sec"] == 3.0


def test_speed_classification():
    result = prepare_benchmark(get_test_data())

    nova = result[result["model"] == "Nova-7B"].iloc[0]
    border = result[result["model"] == "BorderModel"].iloc[0]
    atlas = result[result["model"] == "Atlas-Agent"].iloc[0]

    assert nova["speed_class"] == "fast"
    assert border["speed_class"] == "slow"
    assert atlas["speed_class"] == "slow"


def test_sorted_by_latency():
    result = prepare_benchmark(get_test_data())

    assert result["latency_sec"].is_monotonic_increasing
