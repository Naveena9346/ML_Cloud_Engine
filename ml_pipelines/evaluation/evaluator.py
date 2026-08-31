from typing import Any, Dict
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, precision_score, r2_score, recall_score, roc_auc_score, confusion_matrix


class ModelEvaluatorEngine:
    """Evaluation metrics calculator for Classification and Regression models."""

    @staticmethod
    def evaluate_classification(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray = None) -> Dict[str, Any]:
        """Calculate Accuracy, Precision, Recall, F1, ROC-AUC, and Confusion Matrix."""
        acc = float(accuracy_score(y_true, y_pred))
        prec = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
        rec = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
        f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
        
        cm = confusion_matrix(y_true, y_pred).tolist()
        
        roc_auc = None
        if y_proba is not None:
            try:
                if y_proba.ndim == 2 and y_proba.shape[1] == 2:
                    roc_auc = float(roc_auc_score(y_true, y_proba[:, 1]))
                else:
                    roc_auc = float(roc_auc_score(y_true, y_proba, multi_class="ovr"))
            except Exception:
                roc_auc = None

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4) if roc_auc is not None else None,
            "confusion_matrix": cm
        }

    @staticmethod
    def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Calculate MSE, RMSE, MAE, and R2 Score."""
        mse = float(mean_squared_error(y_true, y_pred))
        rmse = float(np.sqrt(mse))
        mae = float(mean_absolute_error(y_true, y_pred))
        r2 = float(r2_score(y_true, y_pred))

        return {
            "mse": round(mse, 4),
            "rmse": round(rmse, 4),
            "mae": round(mae, 4),
            "r2_score": round(r2, 4)
        }
