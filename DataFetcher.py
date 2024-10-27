from typing import Dict, Any
import time

class DataFetcher:
    def __init__(self, APIKey: str, baseURL: str, timeout: int):
        self.APIKey = APIKey
        self.baseURL = baseURL
        self.timeout = timeout

    def fetchData(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetches data from an API using specified parameters.
        Tries up to 3 retries if data validation fails.
        """
        response = {"status": "success", "data": {"key": "value"}}  # Placeholder for actual API call
        for retry in range(3):  # Retry up to 3 times
            if self.validateResponse(response):
                return self.formatData(response)
            else:
                self.retryOnFailure(3)  # Retry on failure
        return {}

    def validateResponse(self, response: Dict[str, Any]) -> bool:
        """
        Checks if the API response status is 'success'.
        """
        return response.get("status") == "success"

    def formatData(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats the response data to a JSON format suitable for processing.
        Extracts the 'data' field from the response.
        """
        return response.get("data", {})

    def handleAPIRateLimit(self) -> None:
        """
        Pauses execution to handle API rate limit.
        """
        print("Rate limit reached, waiting to retry...")
        time.sleep(60)

    def retryOnFailure(self, retries: int) -> Dict[str, Any]:
        """
        Attempts to fetch data multiple times on failure.
        """
        for attempt in range(retries):
            data = self.fetchData({})
            if data:
                return data
            self.handleAPIRateLimit()  # Wait before retrying
        return {}