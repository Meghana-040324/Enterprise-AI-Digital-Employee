# incident_service.py
import requests
from requests.auth import HTTPBasicAuth

from config import (
    SERVICENOW_URL,
    SERVICENOW_USER,
    SERVICENOW_PASSWORD
)

from utils.logger import get_logger


logger = get_logger(__name__)


class IncidentService:

    def create_incident(
        self,
        short_description: str,
        description: str = "",
        urgency: str = "2",
        impact: str = "2"
    ):

        if not SERVICENOW_URL:

            return {
                "success": False,
                "message": "ServiceNow URL is missing."
            }

        if not SERVICENOW_USER:

            return {
                "success": False,
                "message": "ServiceNow username is missing."
            }

        if not SERVICENOW_PASSWORD:

            return {
                "success": False,
                "message": "ServiceNow password is missing."
            }

        url = (
            f"{SERVICENOW_URL}"
            "/api/now/table/incident"
        )

        payload = {

            "short_description":
                short_description,

            "description":
                description or
                "Created automatically by "
                "Enterprise AI Digital Employee",

            "urgency":
                urgency,

            "impact":
                impact
        }

        headers = {

            "Accept":
                "application/json",

            "Content-Type":
                "application/json"
        }

        try:

            response = requests.post(

                url,

                auth=HTTPBasicAuth(
                    SERVICENOW_USER,
                    SERVICENOW_PASSWORD
                ),

                headers=headers,

                json=payload,

                timeout=20
            )

            logger.info(
                "ServiceNow status=%s",
                response.status_code
            )

            if response.status_code == 201:

                result = (
                    response.json()
                    .get(
                        "result",
                        {}
                    )
                )

                return {

                    "success": True,

                    "number":
                        result.get("number"),

                    "sys_id":
                        result.get("sys_id"),

                    "message":
                        "Incident created successfully."
                }

            return {

                "success": False,

                "message":
                    f"ServiceNow returned "
                    f"HTTP {response.status_code}: "
                    f"{response.text[:500]}"
            }

        except requests.RequestException as exc:

            logger.exception(
                "ServiceNow connection failed."
            )

            return {

                "success": False,

                "message":
                    f"ServiceNow connection error: "
                    f"{str(exc)}"
            }


incident_service = IncidentService()