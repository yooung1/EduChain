from fastapi import HTTPException, Depends, status
from app.constants.user_registration_model_constants import UserRole


# TODO: adicionar JWT que vai trazer o User, assim vamos poder pegar usuario logado e ver o seu tipo

class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.user_type not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para realizer esta ação"
            )

        return user