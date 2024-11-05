import time

class MemoryObject:
    message: str
    role: str
    timestamp: int

    def __init__(self, message: str, role: str):
        self.message = message
        self.role = role
        self.timestamp = int(time.time()) 


class Memory:
    session: dict[str, list[MemoryObject]] = {}
    window_size = 10

    def add_message(self, session_id: str, message: str, role: str):
        if session_id not in self.session:
            self.session[session_id] = []  # Initialize with an empty list

        mem_obj = MemoryObject(message, role)
        self.session[session_id].append(mem_obj)
        # Keep only the last `window_size` messages
        self.session[session_id] = self.session[session_id][-self.window_size:]

    def get_session(self, session_id: str) -> list[MemoryObject]:
        if session_id not in self.session:
            self.session[session_id] = []  # Initialize with an empty list
        return self.session[session_id]
    
    def clear_session(self, session_id: str) -> list[MemoryObject]:
        if session_id not in self.session:
            self.session[session_id] = []  # Initialize with an empty list
        self.session[session_id] = [] 