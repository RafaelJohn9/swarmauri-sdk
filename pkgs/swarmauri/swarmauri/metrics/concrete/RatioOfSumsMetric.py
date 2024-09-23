from typing import Any, Literal
import pandas as pd

from swarmauri.metrics.base.MetricBase import MetricBase
from swarmauri.metrics.base.MetricCalculateMixin import MetricCalculateMixin


class RatioOfSumsMetric(MetricBase, MetricCalculateMixin):
    """
    A metric class to calculate the ratio of the sum of two columns in a DataFrame.
    """

    type: Literal["RatioOfSumsMetric"] = "RatioOfSumsMetric"

    def calculate(self, data: pd.DataFrame, column_a: str, column_b: str) -> float:
        """
        Calculate the ratio of the sum of two columns in a DataFrame.

        Parameters:
            data (pd.DataFrame): The input DataFrame.
            column_a (str): The name of the first column.
            column_b (str): The name of the second column.

        Returns:
            float: The ratio of the sum of the two columns.
        """
        sum_a = data[column_a].sum()
        sum_b = data[column_b].sum()

        if sum_b == 0:
            raise ValueError(
                f"The sum of column '{column_b}' is zero, cannot divide by zero."
            )

        return sum_a / sum_b
