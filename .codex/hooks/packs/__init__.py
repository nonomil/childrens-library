"""hooks packs 注册表。"""

from packs.context.rules import build_context_rules
from packs.git.rules import build_git_rules
from packs.notify.rules import build_notify_rules
from packs.quality.rules import build_quality_rules
from packs.resilience.rules import build_resilience_rules
from packs.security.rules import build_security_rules
from packs.validate.rules import build_validate_rules

PACK_BUILDERS = {
    "context": build_context_rules,
    "git": build_git_rules,
    "notify": build_notify_rules,
    "quality": build_quality_rules,
    "security": build_security_rules,
    "resilience": build_resilience_rules,
    "validate": build_validate_rules,
}

__all__ = ["PACK_BUILDERS"]
