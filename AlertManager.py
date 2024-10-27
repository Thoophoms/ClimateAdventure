from typing import List, Dict, Any
from datetime import datetime

class AlertManager:
    def __init__(self, notificationType: str):
        self.thresholds = {}
        self.notificationType = notificationType

    def setAlertThresholds(self, parameters: Dict[str, Any]) -> None:
        """
        Sets threshold limits for climate metrics.
        """
        self.thresholds = parameters

    def checkAlerts(self, data: Dict[str, Any]) -> List[str]:
        """
        Checks if data meets alert conditions.
        """
        alerts = [key for key, value in data.items() if value > self.thresholds.get(key, float("inf"))]
        return alerts

    def notifyUser(self, alerts: List[str]) -> None:
        """
        Notifies the user of alerts.
        """
        print("Notifying user of alerts:", alerts)

    def configureNotificationPreferences(self, preferences: Dict[str, Any]) -> None:
        """
        Configures notification settings.
        """
        self.notificationType = preferences.get("notificationType", self.notificationType)

    def logAlertHistory(self, alertID: str, timestamp: datetime) -> None:
        """
        Logs triggered alerts for historical tracking.
        """
        print(f"Logging alert {alertID} at {timestamp}")

    def clearAlerts(self) -> None:
        """
        Clears all set alerts.
        """
        print("Clearing all alerts")