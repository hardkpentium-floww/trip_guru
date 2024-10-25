from datetime import datetime, timedelta

from trip.interactors.storage_interfaces.storage_interface import StorageInterface, AccessTokenDTO, RefreshTokenDTO, \
    AuthenticationTokensDTO
from django.http import JsonResponse

from trip.storages.storage_implementation import StorageImplementation


class LoginInteractor:

    def __init__(self, storage: StorageImplementation):
        self.storage = storage


    def login(self,
                 user_id: str,
                 ) :
        access_token_str = "access_token"
        refresh_token_str = "refresh_token"
        expires = datetime.now() + timedelta(hours=1)
        # user = UserAccount.objects.get(user_id=user_id)
        access_token_dto = AccessTokenDTO(
            user_id=user_id,
            token=access_token_str,
            application_name="trip-guru",
            expires=expires,
            scope='read write',
            source_refresh_token=""
        )

        access_token = self.storage.create_access_token(
           access_token_dto=access_token_dto)

        refresh_token_dto = RefreshTokenDTO(
            user_id=user_id,
            token=refresh_token_str,
            application_name="trip-guru",
            access_token_id=access_token.id
        )
        refresh_token = self.storage.create_refresh_token(
            refresh_token_dto=refresh_token_dto
        )

        self.storage.validate_user_id(user_id=user_id)

        login_dto = AuthenticationTokensDTO(
            access_token=access_token_str,
            expires_in=expires,
            token_type="Bearer",
            scope="read write",
            refresh_token=refresh_token_str
        )

        login_response = {
            "access_token": login_dto.access_token,
            "expires_in": login_dto.expires_in,
            "token_type": login_dto.token_type,
            "scope": login_dto.scope,
            "refresh_token": login_dto.refresh_token
        }

        return JsonResponse(data=login_response, status=200)


