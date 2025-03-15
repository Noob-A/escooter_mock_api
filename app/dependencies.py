from fastapi import Header, HTTPException

def get_current_user_id(x_user_id: int = Header(...)):
    # In a real system, you would verify an authentication token.
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header missing")
    return x_user_id
