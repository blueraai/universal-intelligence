"""Universal Intelligence package."""

from . import community, core

# default models, tools, agents for playground
from .community.models.default import UniversalModel as Model
from .community.tools.default import UniversalTool as Tool
from .community.agents.default import UniversalAgent as Agent
from .community.agents.default import UniversalAgent as OtherAgent

__all__ = ["core", "community", "Model", "Tool", "Agent", "OtherAgent"]
