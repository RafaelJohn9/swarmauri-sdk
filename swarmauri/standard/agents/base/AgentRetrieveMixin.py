from abc import ABC
from typing import List
from pydantic import BaseModel, ConfigDict, field_validator, Field
from swarmauri.core.documents.IDocument import IDocument
from swarmauri.core.agents.IAgentRetrieve import IAgentRetrieve

class AgentRetrieveMixin(IAgentRetrieve, BaseModel):
    last_retrieved: List[IDocument] = Field(default_factory=list)
    model_config = ConfigDict(extra='forbid', arbitrary_types_allowed=True)
