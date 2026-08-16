# memory_service.py
from collections import defaultdict
from threading import Lock

from config import MAX_MEMORY_MESSAGES


class MemoryService:

    def __init__(self):

        self.sessions = defaultdict(list)

        self.lock = Lock()

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        with self.lock:

            self.sessions[session_id].append(
                {
                    "role": role,
                    "content": content
                }
            )

            self.sessions[session_id] = (
                self.sessions[session_id][-MAX_MEMORY_MESSAGES:]
            )

    def get_history(
        self,
        session_id: str
    ):

        with self.lock:

            return list(
                self.sessions.get(
                    session_id,
                    []
                )
            )

    def clear(
        self,
        session_id: str
    ):

        with self.lock:

            self.sessions.pop(
                session_id,
                None
            )


memory_service = MemoryService()