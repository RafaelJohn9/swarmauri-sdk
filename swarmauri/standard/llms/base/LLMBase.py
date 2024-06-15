from abc import ABC, abstractmethod
from typing import Any, Union, Optional
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator
from swarmauri.core.ComponentBase import ComponentBase, ResourceTypes
from swarmauri.core.models.IPredict import IPredict

class LLMBase(IPredict, ComponentBase):
    allowed_models: List[str] = []
    resource: Optional[str] =  Field(default=ResourceTypes.LLM.value, frozen=True)
    model_config = ConfigDict(extra='forbid', arbitrary_types_allowed=True)

    @model_validator(mode='after')
    @classmethod
    def _validate_name_in_allowed_models(cls, values):
        name = values.name
        allowed_models = values.allowed_models
        if name and name not in allowed_models:
            raise ValueError(f"Model name {name} is not allowed. Choose from {allowed_models}")
        return values
        
    def predict(self, *args, **kwargs):
        raise NotImplementedError('Predict not implemented in subclass yet.')
        