import os
import jwt
from datetime import datetime, timedelta, timezone
import uuid


CONTROL_UNIT_SECRET_KEY = os.getenv("CONTROL_UNIT_SECRET_KEY")
ALGORITHM = "HS256"

mock_unit_id = str(uuid.uuid4())
# mock_unit_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479"

payload = {"unit_id": mock_unit_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=30)}

token = jwt.encode(payload, CONTROL_UNIT_SECRET_KEY, algorithm=ALGORITHM)
print("Your mocked jwt is:\n")
print(token)
print("\nUse this unit ID in the body:\n", mock_unit_id)
