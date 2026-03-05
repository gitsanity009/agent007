from python.helpers import git, runtime
import hashlib

async def check_version():
    # External update checks disabled for classified environment
    # No outbound network calls to external services
    current_version = git.get_version()
    return {"current_version": current_version, "latest_version": current_version, "update_available": False}