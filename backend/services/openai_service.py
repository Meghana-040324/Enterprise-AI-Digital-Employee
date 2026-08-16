# openai_service.py
from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL
)

from services.memory_service import (
    memory_service
)

from services.rag_service import (
    rag_service
)


SYSTEM_PROMPTS = {

    "enterprise":
        """
You are Enterprise AI Digital Employee.

You assist employees with IT,
HR, operations, enterprise software,
company documents and workplace requests.

Be professional, concise and helpful.

When document context is supplied,
prefer that context over general knowledge.

Never claim an enterprise action was
completed unless the application confirms it.
""",

    "it":
        """
You are an enterprise IT Support Agent.

Help employees troubleshoot laptops,
VPNs, Wi-Fi, email, passwords,
software and enterprise applications.

Give clear step-by-step instructions.
""",

    "hr":
        """
You are an enterprise HR Assistant.

Help employees understand workplace
processes, policies, leave requests
and HR documentation.

Do not invent company policy.
""",

    "servicenow":
        """
You are a ServiceNow Expert Assistant.

Help with ServiceNow administration,
development, workflows, scripting,
ITSM and troubleshooting.
""",

    "finance":
        """
You are an enterprise Finance Assistant.

Help explain business finance processes
and supplied financial documents.

Do not fabricate financial records.
"""
}


class OpenAIService:

    def __init__(self):

        self.client = None

        if OPENAI_API_KEY:

            self.client = OpenAI(
                api_key=OPENAI_API_KEY
            )

    def _ensure_client(self):

        if not self.client:

            raise RuntimeError(
                "OPENAI_API_KEY is missing."
            )

    def detect_action(
        self,
        prompt: str
    ):

        text = prompt.lower()

        incident_phrases = [

            "not working",
            "isn't working",
            "doesn't work",
            "cannot login",
            "can't login",
            "unable to login",
            "vpn issue",
            "wifi issue",
            "network issue",
            "printer issue",
            "laptop issue",
            "email issue",
            "outlook issue",
            "software issue"
        ]

        if any(
            phrase in text
            for phrase
            in incident_phrases
        ):

            return "incident"

        return "chat"

    def generate_response(
        self,
        prompt: str,
        session_id: str,
        persona: str = "enterprise"
    ):

        self._ensure_client()

        history = (
            memory_service
            .get_history(
                session_id
            )
        )

        context_results = (
            rag_service
            .search(
                prompt
            )
        )

        context = ""

        if context_results:

            context = (
                "\n\nRelevant company "
                "document context:\n"
            )

            for item in context_results:

                context += (
                    f"\nSOURCE: "
                    f"{item['filename']}\n"
                    f"{item['content']}\n"
                )

        instructions = (
            SYSTEM_PROMPTS.get(
                persona,
                SYSTEM_PROMPTS[
                    "enterprise"
                ]
            )
        )

        if context:

            instructions += context

        input_messages = []

        for message in history:

            input_messages.append(
                {
                    "role":
                        message["role"],

                    "content":
                        message["content"]
                }
            )

        input_messages.append(
            {
                "role":
                    "user",

                "content":
                    prompt
            }
        )

        response = (
            self.client.responses.create(

                model=
                    OPENAI_MODEL,

                instructions=
                    instructions,

                input=
                    input_messages
            )
        )

        answer = (
            response.output_text
            or
            "I could not generate a response."
        )

        memory_service.add_message(
            session_id,
            "user",
            prompt
        )

        memory_service.add_message(
            session_id,
            "assistant",
            answer
        )

        return answer


openai_service = OpenAIService()