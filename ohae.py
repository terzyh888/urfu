import numpy as np
import pandas as pd


def prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["cost_per_1k_tokens"] = (
        result["cost_usd"] / result["total_tokens"] * 1000
    )
    result["cost_class"] = np.select(
        [
            result["cost_usd"] < 0.02,
            result["cost_usd"] < 0.06,
        ],
        ["cheap", "normal"],
        default="expensive",
    )

    result = result.drop(columns=["cost_usd"])
    result = result.sort_values("cost_per_1k_tokens")

    return result


if __name__ == "__main__":
    data = pd.read_csv("data/benchmark.csv")
    print(prepare_benchmark(data))
