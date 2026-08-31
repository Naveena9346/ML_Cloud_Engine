from enum import Enum
from typing import List, Set, Union
from fastapi import HTTPException, status, Depends
from pydantic import BaseModel


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    ML_ENGINEER = "ML_ENGINEER"
    DATA_SCIENTIST = "DATA_SCIENTIST"
    DATA_ENGINEER = "DATA_ENGINEER"
    DEVELOPER = "DEVELOPER"
    VIEWER = "VIEWER"


class Permission(str, Enum):
    # System Administration
    MANAGE_SYSTEM_SETTINGS = "system:manage_settings"
    MANAGE_ALL_USERS = "users:manage_all"
    
    # Workspace & Projects
    CREATE_WORKSPACE = "workspace:create"
    DELETE_WORKSPACE = "workspace:delete"
    MANAGE_WORKSPACE_MEMBERS = "workspace:manage_members"
    CREATE_PROJECT = "project:create"
    DELETE_PROJECT = "project:delete"
    VIEW_PROJECT = "project:view"
    
    # Dataset Management & Feature Store
    UPLOAD_DATASET = "dataset:upload"
    DELETE_DATASET = "dataset:delete"
    CLEAN_DATASET = "dataset:clean"
    RUN_EDA = "dataset:eda"
    MANAGE_FEATURE_STORE = "features:manage"
    VIEW_DATASET = "dataset:view"
    
    # Model Training & Experiments
    START_TRAINING_JOB = "training:start"
    CANCEL_TRAINING_JOB = "training:cancel"
    DELETE_EXPERIMENT = "training:delete_experiment"
    VIEW_TRAINING_METRICS = "training:view_metrics"
    
    # Model Registry & Lifecycle
    REGISTER_MODEL = "model:register"
    APPROVE_MODEL_PROMOTION = "model:approve_promotion"
    DELETE_MODEL = "model:delete"
    VIEW_MODEL_REGISTRY = "model:view_registry"
    
    # Model Serving & Deployment
    DEPLOY_MODEL_ENDPOINT = "deployment:deploy"
    UNDEPLOY_MODEL_ENDPOINT = "deployment:undeploy"
    INVOKE_PREDICTION_API = "prediction:invoke"
    VIEW_DEPLOYMENTS = "deployment:view"
    
    # Monitoring & Telemetry
    VIEW_MONITORING_DASHBOARD = "monitoring:view"
    MANAGE_DRIFT_ALERTS = "monitoring:manage_alerts"
    VIEW_AUDIT_LOGS = "audit:view"


# Role-Permission Mapping Matrix
ROLE_PERMISSIONS: dict[UserRole, Set[Permission]] = {
    UserRole.SUPER_ADMIN: set(Permission),  # All permissions
    
    UserRole.ADMIN: {
        Permission.MANAGE_ALL_USERS,
        Permission.CREATE_WORKSPACE,
        Permission.MANAGE_WORKSPACE_MEMBERS,
        Permission.CREATE_PROJECT,
        Permission.DELETE_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.UPLOAD_DATASET,
        Permission.DELETE_DATASET,
        Permission.CLEAN_DATASET,
        Permission.RUN_EDA,
        Permission.MANAGE_FEATURE_STORE,
        Permission.VIEW_DATASET,
        Permission.START_TRAINING_JOB,
        Permission.CANCEL_TRAINING_JOB,
        Permission.DELETE_EXPERIMENT,
        Permission.VIEW_TRAINING_METRICS,
        Permission.REGISTER_MODEL,
        Permission.APPROVE_MODEL_PROMOTION,
        Permission.DELETE_MODEL,
        Permission.VIEW_MODEL_REGISTRY,
        Permission.DEPLOY_MODEL_ENDPOINT,
        Permission.UNDEPLOY_MODEL_ENDPOINT,
        Permission.INVOKE_PREDICTION_API,
        Permission.VIEW_DEPLOYMENTS,
        Permission.VIEW_MONITORING_DASHBOARD,
        Permission.MANAGE_DRIFT_ALERTS,
        Permission.VIEW_AUDIT_LOGS,
    },
    
    UserRole.ML_ENGINEER: {
        Permission.CREATE_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.UPLOAD_DATASET,
        Permission.CLEAN_DATASET,
        Permission.RUN_EDA,
        Permission.MANAGE_FEATURE_STORE,
        Permission.VIEW_DATASET,
        Permission.START_TRAINING_JOB,
        Permission.CANCEL_TRAINING_JOB,
        Permission.VIEW_TRAINING_METRICS,
        Permission.REGISTER_MODEL,
        Permission.APPROVE_MODEL_PROMOTION,
        Permission.VIEW_MODEL_REGISTRY,
        Permission.DEPLOY_MODEL_ENDPOINT,
        Permission.UNDEPLOY_MODEL_ENDPOINT,
        Permission.INVOKE_PREDICTION_API,
        Permission.VIEW_DEPLOYMENTS,
        Permission.VIEW_MONITORING_DASHBOARD,
        Permission.MANAGE_DRIFT_ALERTS,
        Permission.VIEW_AUDIT_LOGS,
    },
    
    UserRole.DATA_SCIENTIST: {
        Permission.CREATE_PROJECT,
        Permission.VIEW_PROJECT,
        Permission.UPLOAD_DATASET,
        Permission.CLEAN_DATASET,
        Permission.RUN_EDA,
        Permission.MANAGE_FEATURE_STORE,
        Permission.VIEW_DATASET,
        Permission.START_TRAINING_JOB,
        Permission.CANCEL_TRAINING_JOB,
        Permission.VIEW_TRAINING_METRICS,
        Permission.REGISTER_MODEL,
        Permission.VIEW_MODEL_REGISTRY,
        Permission.INVOKE_PREDICTION_API,
        Permission.VIEW_DEPLOYMENTS,
        Permission.VIEW_MONITORING_DASHBOARD,
    },
    
    UserRole.DATA_ENGINEER: {
        Permission.VIEW_PROJECT,
        Permission.UPLOAD_DATASET,
        Permission.DELETE_DATASET,
        Permission.CLEAN_DATASET,
        Permission.RUN_EDA,
        Permission.MANAGE_FEATURE_STORE,
        Permission.VIEW_DATASET,
        Permission.VIEW_TRAINING_METRICS,
        Permission.INVOKE_PREDICTION_API,
        Permission.VIEW_DEPLOYMENTS,
        Permission.VIEW_MONITORING_DASHBOARD,
    },
    
    UserRole.DEVELOPER: {
        Permission.VIEW_PROJECT,
        Permission.VIEW_DATASET,
        Permission.VIEW_MODEL_REGISTRY,
        Permission.DEPLOY_MODEL_ENDPOINT,
        Permission.INVOKE_PREDICTION_API,
        Permission.VIEW_DEPLOYMENTS,
        Permission.VIEW_MONITORING_DASHBOARD,
    },
    
    UserRole.VIEWER: {
        Permission.VIEW_PROJECT,
        Permission.VIEW_DATASET,
        Permission.VIEW_TRAINING_METRICS,
        Permission.VIEW_MODEL_REGISTRY,
        Permission.VIEW_DEPLOYMENTS,
        Permission.VIEW_MONITORING_DASHBOARD,
    },
}


class RoleChecker:
    """Dependency for validating user role access against required permissions."""
    
    def __init__(self, allowed_roles: List[UserRole] = None, required_permissions: List[Permission] = None):
        self.allowed_roles = allowed_roles or []
        self.required_permissions = required_permissions or []

    def __call__(self, current_user_role: str):
        role_enum = UserRole(current_user_role)
        
        # Check explicit role requirement
        if self.allowed_roles and role_enum not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{current_user_role}' is not authorized to perform this operation."
            )
            
        # Check required permissions
        user_perms = ROLE_PERMISSIONS.get(role_enum, set())
        for perm in self.required_permissions:
            if perm not in user_perms:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{perm.value}' required for role '{current_user_role}'."
                )
        return True
