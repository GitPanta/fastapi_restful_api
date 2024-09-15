from enum import Enum

class UserRole(Enum):
    super_admin = "super_admin"
    admin = "admin"
    user = "user"