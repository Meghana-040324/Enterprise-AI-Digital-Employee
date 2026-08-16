# analytics_service.py
from collections import defaultdict
from threading import Lock


class AnalyticsService:

    def __init__(self):

        self.lock = Lock()

        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

        self.incidents_created = 0
        self.documents_uploaded = 0

        self.total_response_time_ms = 0.0

        self.action_counts = defaultdict(int)

    def record_request(
        self,
        success: bool,
        execution_time_ms: float,
        action: str = "chat"
    ):

        with self.lock:

            self.total_requests += 1

            self.total_response_time_ms += execution_time_ms

            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1

            self.action_counts[action] += 1

    def record_incident(self):

        with self.lock:

            self.incidents_created += 1

    def record_document(self):

        with self.lock:

            self.documents_uploaded += 1

    def get_stats(self):

        with self.lock:

            average = 0

            if self.total_requests:

                average = (
                    self.total_response_time_ms /
                    self.total_requests
                )

            return {

                "total_requests":
                    self.total_requests,

                "successful_requests":
                    self.successful_requests,

                "failed_requests":
                    self.failed_requests,

                "incidents_created":
                    self.incidents_created,

                "documents_uploaded":
                    self.documents_uploaded,

                "average_response_time_ms":
                    round(average, 2),

                "action_counts":
                    dict(self.action_counts)
            }


analytics_service = AnalyticsService()