import pandas as pd
from ml_pipelines.preprocessing.eda import EDAEngine


def test_eda_engine_summary_generation():
    """Test automated Exploratory Data Analysis statistical profiling engine."""
    data = {
        "age": [25, 30, 35, 40, None, 50, 55],
        "income": [50000, 60000, 75000, 90000, 110000, 130000, 150000],
        "category": ["A", "B", "A", "C", "B", "A", None]
    }
    df = pd.DataFrame(data)
    
    eda = EDAEngine(df)
    summary = eda.generate_summary()
    
    assert "overview" in summary
    assert summary["overview"]["total_rows"] == 7
    assert summary["overview"]["total_columns"] == 3
    assert summary["overview"]["missing_cells"] == 2
    assert "age" in summary["column_summaries"]
    assert summary["column_summaries"]["age"]["mean"] is not None
