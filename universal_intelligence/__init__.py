"""Universal Intelligence package."""

from . import community, core
from .community.agents.default import UniversalAgent as Agent
from .community.agents.default import UniversalAgent as OtherAgent

# default models, tools, agents for playground
from .community.models.local.default import UniversalModel as Model
from .community.models.remote.default import UniversalModel as RemoteModel
from .community.tools.default import UniversalTool as Tool

__all__ = ["core", "community", "Model", "Tool", "Agent", "OtherAgent", "RemoteModel"]
