from src.app.user.model import User
from src.db.manager import BaseManager

class UserManager(BaseManager):
    def __init__(self):
        super().__init__(User)
