from dataclasses import dataclass
from typing import List
from abc import abstractmethod
from datetime import datetime


@dataclass()
class DestinationDTO:
    id: int
    name: str
    description: str
    tags: str
    user_id: str

@dataclass()
class MutateDestinationDTO:
    destination_id: int = None
    name: str = None
    description: str = None
    tags: str= None
    user_id: str= None

@dataclass()
class HotelDTO:
    id: int
    name: str
    description: str
    tariff: int
    image_urls: str
    destination_id: int

@dataclass()
class MutateHotelDTO:
    hotel_id: int = None
    name: str= None
    description: str= None
    tariff: int= None
    image_urls: str= None
    destination_id: int= None


@dataclass()
class RatingDTO:
    id: int
    rating: int
    user_id: str
    review: str
    destination_id: int


@dataclass()
class MutateRatingDTO:
    rating: int= None
    user_id: str= None
    review: str= None
    destination_id: int= None


@dataclass()
class UserDTO:
    id: str
    name: str
    phone_no: str


@dataclass()
class BookingDTO:
    booking_id: int
    hotel_id: int
    user_id: str
    destination_id: int
    checkin_date: str
    checkout_date: str
    total_amount: int

@dataclass()
class MutateBookingDTO:
    booking_id: int = None
    hotel_id: int= None
    user_id: str= None
    destination_id: int= None
    checkin_date: str= None
    checkout_date: str= None
    total_amount: int= None

@dataclass()
class GetDestinationsDTO:
  offset : int
  limit : int
  tag : str


@dataclass()
class SearchDestinationDTO:
    name: str
    offset : int
    limit : int
    tag:str

@dataclass()
class UpdateBookingDTO:
    booking_id: int
    user_id: str
    checkin_date: str= None
    checkout_date: str= None


@dataclass()
class AccessTokenDTO:
    user_id :str
    token :str
    application_name:str
    expires:datetime
    scope :str  # Define the scope based on your requirement
    source_refresh_token :str


@dataclass()
class RefreshTokenDTO:
    user_id :str
    token :str
    application_name:str
    access_token_id: int

@dataclass()
class AuthenticationTokensDTO:
    access_token: str
    refresh_token: str
    expires_in: datetime
    scope: str
    token_type: str


@dataclass()
class BookHotelDTO:
    user_id: str
    hotel_id: int
    checkin_date: str
    checkout_date: str
    total_amount: int
    tariff : int
    destination_id: int



class StorageInterface:
    @abstractmethod
    def add_destination(self, add_destination_dto: MutateDestinationDTO)->DestinationDTO :
        pass

    @abstractmethod
    def validate_destination_id(self, destination_id: int):
        pass

    @abstractmethod
    def search_destination(self, search_destination_dto: SearchDestinationDTO)-> List[DestinationDTO]:
        pass

    @abstractmethod
    def create_refresh_token(self,
                             refresh_token_dto: RefreshTokenDTO):
        pass

    @abstractmethod
    def create_access_token(self,
                            access_token_dto: AccessTokenDTO):
        pass

    @abstractmethod
    def validate_user_id(self, user_id:str):
        pass

    @abstractmethod
    def logout(self, user_id: int):
        pass

    @abstractmethod
    def get_application_instance(self, application_name: str):
        pass

    @abstractmethod
    def get_user_account(self, user_id: str):
        pass

    @abstractmethod
    def validate_admin_user(self, user_id: str):
        pass

    @abstractmethod
    def validate_hotel_customer(self,destination_id: int, user_id: str):
        pass

    @abstractmethod
    def get_destination(self, destination_id: int)->DestinationDTO:
        pass

    @abstractmethod
    def get_destinations(self, get_destinations_dto: GetDestinationsDTO)-> List[DestinationDTO]:
        pass

    @abstractmethod
    def add_hotel(self,user_id: str, add_hotel_dto: MutateHotelDTO):
        pass

    @abstractmethod
    def get_hotel(self, hotel_id: int)->HotelDTO    :
        pass

    @abstractmethod
    def add_rating(self, add_rating_dto: MutateRatingDTO):
        pass

    @abstractmethod
    def book_hotel(self,hotel_id: int, book_hotel_dto: MutateBookingDTO):
        pass

    @abstractmethod
    def update_booking(self, booking_id: int, update_booking_dto: MutateBookingDTO)->BookingDTO:
        pass

    @abstractmethod
    def update_destination(self, destination_id: int, update_destination_dto: MutateDestinationDTO)->DestinationDTO:
        pass

    @abstractmethod
    def update_hotel(self,hotel_id: int, update_hotel_dto: MutateHotelDTO)->HotelDTO:
        pass

    @abstractmethod
    def get_hotels(self, destination_id: int) -> List[HotelDTO]:
        pass

    @abstractmethod

    def get_bookings_for_user(self, user_id: str, offset: int, limit: int) -> List[BookingDTO]:
        pass

    # def get_user(self, user_id: str):
    #     pass

# @dataclass()
# class UpdateDestinationDTO:
#     destination_id: int
#     name: str
#     description: str
#     image_urls: List[str]
#     user_id: str
#     tags: List[str]
#
#
# @dataclass()
# class UpdateHotelDTO:
#     hotel_id: int
#     name: str
#     description: str
#     image_urls: List[str]
#     user_id: str
#     tags: List[str]
#
#


# @dataclass()
# class GetDestinationDTO:
#     destination_name: str


