import pandas as pd
from ml_pipelines.evaluation.evaluator import ModelEvaluatorEngine
from ml_pipelines.training.trainer import ModelTrainerEngine


def test_model_training_and_evaluation():
    """Test model training execution and evaluation metric computation."""
    df = pd.DataFrame({
        "feature1": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        "feature2": [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
        "target": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    })
    
    trainer = ModelTrainerEngine(df, target_column="target", model_type="CLASSIFICATION")
    model, results, X_train, y_train = trainer.train(algorithm="RANDOM_FOREST", params={"n_estimators": 10})
    
    assert model is not None
    assert len(results["y_pred"]) == len(results["y_test"])
    
    metrics = ModelEvaluatorEngine.evaluate_classification(results["y_test"], results["y_pred"], results["y_proba"])
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "confusion_matrix" in metrics
