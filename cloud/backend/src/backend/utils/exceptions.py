from fastapi import HTTPException, status

def UnauthorizedException(detail: str, headers: dict):
  return HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=detail,
    headers=headers,
  )

def BadRequestException(detail: str):
  return HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=detail,
  )

def InternalServerException(detail: str):
  return HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail=detail,
  )  