from typing import Any, Dict
import optuna
import pandas as pd
from sklearn.model_selection import cross_val_score
from ml_pipelines.training.trainer import ModelTrainerEngine


class OptunaTunerEngine:
    """Hyperparameter Tuning Engine utilizing Optuna Bayesian Optimization."""

    def __init__(self, df: pd.DataFrame, target_column: str, algorithm: str, model_type: str = "CLASSIFICATION"):
        self.df = df
        self.target_column = target_column
        self.algorithm = algorithm.upper()
        self.model_type = model_type.upper()
        self.trainer_engine = ModelTrainerEngine(df, target_column, model_type)

    def _objective(self, trial: optuna.Trial) -> float:
        """Optuna objective trial callback."""
        params = {}
        if self.algorithm == "RANDOM_FOREST":
            params["n_estimators"] = trial.suggest_int("n_estimators", 10, 200)
            params["max_depth"] = trial.suggest_int("max_depth", 3, 20)
            params["min_samples_split"] = trial.suggest_int("min_samples_split", 2, 10)
        elif self.algorithm == "XGBOOST":
            params["n_estimators"] = trial.suggest_int("n_estimators", 50, 200)
            params["max_depth"] = trial.suggest_int("max_depth", 3, 10)
            params["learning_rate"] = trial.suggest_float("learning_rate", 0.01, 0.3, log=True)
            params["subsample"] = trial.suggest_float("subsample", 0.5, 1.0)
        elif self.algorithm == "LIGHTGBM":
            params["n_estimators"] = trial.suggest_int("n_estimators", 50, 200)
            params["max_depth"] = trial.suggest_int("max_depth", 3, 15)
            params["learning_rate"] = trial.suggest_float("learning_rate", 0.01, 0.3, log=True)

        model = self.trainer_engine.get_model(self.algorithm, params)
        scoring = "accuracy" if self.model_type == "CLASSIFICATION" else "neg_mean_squared_error"
        
        scores = cross_val_score(model, self.trainer_engine.X, self.trainer_engine.y, cv=3, scoring=scoring)
        return float(scores.mean())

    def optimize(self, n_trials: int = 10) -> Dict[str, Any]:
        """Run hyperparameter search and return best parameter set."""
        direction = "maximize" if self.model_type == "CLASSIFICATION" else "maximize"
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        study = optuna.create_study(direction=direction)
        study.optimize(self._objective, n_trials=n_trials)

        return {
            "best_params": study.best_params,
            "best_score": float(study.best_value),
            "n_trials_completed": len(study.trials)
        }
