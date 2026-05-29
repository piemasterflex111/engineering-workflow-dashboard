"""
Classifies Jira issues into operational categories.
"""
import re
from typing import Dict, Any, List


class InfraTicketClassifier:
    """Classifies Jira issues based on content."""

    LINUX_KEYWORDS = ["linux", "ubuntu", "centos", "debian", "kernel", "bash", "ssh", "disk", "mount", "fstab"]
    WINDOWS_KEYWORDS = ["windows", "server", "powershell", "iis", "active directory", "ad", "group policy", "gpo"]
    NETWORK_KEYWORDS = ["network", "dns", "dhcp", "router", "switch", "firewall", "packet loss", "latency", "bandwidth", "tcp", "udp"]

    def classify(self, issue: Dict[str, Any]) -> str:
        """
        Classify an issue into one of the categories:
        - Linux Operations
        - Windows Operations
        - Network Operations
        - Human Review
        """
        summary = issue.get("fields", {}).get("summary", "").lower()
        description = issue.get("fields", {}).get("description", "").lower()
        content = f"{summary} {description}"

        linux_score = sum(1 for kw in self.LINUX_KEYWORDS if kw in content)
        windows_score = sum(1 for kw in self.WINDOWS_KEYWORDS if kw in content)
        network_score = sum(1 for kw in self.NETWORK_KEYWORDS if kw in content)

        if linux_score > windows_score and linux_score > network_score:
            return "Linux Operations"
        elif windows_score > linux_score and windows_score > network_score:
            return "Windows Operations"
        elif network_score > linux_score and network_score > windows_score:
            return "Network Operations"
        else:
            return "Human Review"
