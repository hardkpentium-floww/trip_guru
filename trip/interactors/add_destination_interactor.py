from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidDestination
from trip.interactors.add_hotels_interactor import AddHotelsInteractor
from trip.interactors.storage_interfaces.storage_interface import StorageInterface, DestinationDTO, MutateHotelDTO, \
    MutateDestinationDTO, AddDestinationDTO, AddHotelDTO

from typing import List

class AddDestinationInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_destination(self, add_destination_dto: AddDestinationDTO, add_hotel_dtos: List[AddHotelDTO]):

        check = self.storage.validate_admin_user(user_id=add_destination_dto.user_id)
        if not check:
            raise InvalidAdminUser

        check = self.storage.check_duplicate_destination(add_destination_dto=add_destination_dto)
        if check:
            raise InvalidDestination

        destination_dto = self.storage.add_destination(
            add_destination_dto= add_destination_dto,
        )

        interactor = AddHotelsInteractor(self.storage)
        hotels = interactor.add_hotels(
            add_hotel_dtos=add_hotel_dtos,
            user_id=add_destination_dto.user_id,
            destination_id = destination_dto.id
        )


        return destination_dto
