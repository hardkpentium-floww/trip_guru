from dataclasses import dataclass
from typing import List, Optional
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
class AddDestinationDTO:
    name: str
    description: str
    tags: str
    user_id: str


@dataclass()
class MutateDestinationDTO:
    id:  Optional[int]
    name: Optional[str]
    description: Optional[str]
    tags: Optional[str]
    user_id: Optional[str]

@dataclass()
class HotelDTO:
    id: int
    name: str
    description: str
    tariff: int
    image_urls: str
    destination_id: int

@dataclass()
class AddHotelDTO:
    name: str
    description: str
    tariff: int
    image_urls: str
    destination_id: int

@dataclass()
class MutateHotelDTO:
    hotel_id: int
    name:  Optional[str]
    description:  Optional[str]
    tariff:  Optional[int]
    image_urls:  Optional[str]
    destination_id: Optional[int]



@dataclass()
class RatingDTO:
    id: int
    rating: int
    user_id: str
    review: str
    destination_id: int

@dataclass()
class AddRatingDTO:
    rating: int
    user_id: str
    review: str
    destination_id: int


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
    checkin_date: datetime
    checkout_date: datetime
    total_amount: int

#
# @dataclass()
# class BookHotelDTO:
#     user_id: str
#     hotel_id: int
#     checkin_date: str
#     checkout_date: str
#     total_amount: int
#     tariff : int
#     destination_id: int


@dataclass()
class AddBookingDTO:
    hotel_id: int
    user_id: str
    destination_id: int
    checkin_date: datetime
    checkout_date: datetime
    total_amount: int
    tariff: int

@dataclass()
class MutateBookingDTO:
    booking_id: int
    user_id: str
    hotel_id: int= None
    destination_id: int= None
    checkin_date: datetime= None
    checkout_date: datetime= None
    tariff: int= None
    total_amount: int= None


@dataclass()
class GetDestinationsDTO:
  offset : int
  limit : int
  tag : str



@dataclass()
class AccessTokenDTO:
    user_id :str
    token :str
    application_name:str
    expires:datetime
    scope :str
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




class StorageInterface:
    @abstractmethod
    def add_destination(self, add_destination_dto: AddDestinationDTO)->DestinationDTO :
        pass


    @abstractmethod
    def add_hotels(self, user_id: str, add_hotel_dtos: List[AddHotelDTO],destination_id: int):
        pass

    @abstractmethod
    def validate_destination_id(self, destination_id: int):
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
    def logout(self, user_id: int, access_token:str):
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
    def check_duplicate_destination(self, add_destination_dto):
        pass

    @abstractmethod
    def check_duplicate_hotels(self, add_hotel_dtos: List[AddHotelDTO]):
        pass

    @abstractmethod
    def validate_checkin_checkout_date(self, checkin_date: datetime, checkout_date: datetime):
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
    def add_hotel(self,user_id: str, add_hotel_dto: AddHotelDTO):
        pass

    @abstractmethod
    def get_hotel(self, hotel_id: int)->HotelDTO    :
        pass

    @abstractmethod
    def validate_hotel_id(self, hotel_id: int):
        pass

    @abstractmethod
    def add_rating(self, add_rating_dto: AddRatingDTO):
        pass

    @abstractmethod
    def book_hotel(self,hotel_id: int, book_hotel_dto: AddBookingDTO):
        pass

    @abstractmethod
    def check_overlapping_bookings(self, user_id: str, checkin_date:datetime, checkout_date:datetime):
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
    def get_hotels(self, destination_ids: List[int]) -> List[HotelDTO]:
        pass

    @abstractmethod
    def get_bookings_for_user(self, user_id: str, offset: int, limit: int) -> List[BookingDTO]:
        pass
