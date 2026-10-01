"""Read-only MCP transport for installed corpus releases."""

from .application import McpApplication, main, run_stdio
from .analogs import GeneAnalogIndex
from .binding import ReleaseBinding
from .claims import ClaimGraphIndex
from .compatibility import CompatibilityClaimIndex
from .errors import CorpusToolError
from .policy import CapabilityPolicy
from .service import CorpusService

__all__ = [
    "CapabilityPolicy",
    "ClaimGraphIndex",
    "CompatibilityClaimIndex",
    "CorpusService",
    "CorpusToolError",
    "GeneAnalogIndex",
    "McpApplication",
    "ReleaseBinding",
    "main",
    "run_stdio",
]
