from ninja.orm import create_schema
from .models import User

UserSchema = create_schema(User, exclude=['password', 'is_superuser', 'is_staff'])
