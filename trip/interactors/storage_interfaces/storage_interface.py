from dataclasses import dataclass
from typing import List

@dataclass()
class DestinationDTO:
    id: int
    name: str
    description: str
    tags: str
    user_id: str

@dataclass()
class MutateDestinationDTO:
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
    id: int
    hotel_id: int
    user_id: str
    destination_id: int
    checkin_date: str
    checkout_date: str
    total_amount: int

@dataclass()
class MutateBookingDTO:
    hotel_id: int= None
    user_id: str= None
    destination_id: int= None
    checkin_date: str= None
    checkout_date: str= None
    total_amount: int= None

@dataclass()
class GetDestinationsDTO:
  offset = int
  limit = int
  tag = str


@dataclass()
class UpdateBookingDTO:
    booking_id: int
    user_id: str
    checkin_date: str= None
    checkout_date: str= None

class StorageInterface:
    def add_destination(self, add_destination_dto: MutateDestinationDTO)->DestinationDTO :
        pass

    def validate_admin_user(self, user_id: str):
        pass

    def get_destination(self, destination_id: int)->DestinationDTO:
        pass

    def get_destinations(self, get_destinations_dto: GetDestinationsDTO)-> List[DestinationDTO]:
        pass

    def add_hotel(self, add_hotel_dto: MutateHotelDTO):
        pass

    def get_hotel(self, hotel_id: int)->HotelDTO    :
        pass

    def add_rating(self, add_rating_dto: MutateRatingDTO):
        pass

    def book_hotel(self,hotel_id: int, book_hotel_dto: MutateBookingDTO):
        pass

    def update_booking(self, booking_id: int, update_booking_dto: UpdateBookingDTO)->BookingDTO:
        pass

    def update_destination(self, destination_id: int, update_destination_dto: MutateDestinationDTO)->DestinationDTO:
        pass

    def update_hotel(self,hotel_id: int, update_hotel_dto: MutateHotelDTO)->HotelDTO:
        pass

    def get_hotels(self, destination_id: int) -> List[HotelDTO]:
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
# class BookHotelDTO:
#     user_id: str
#     hotel_id: int
#     checkin_date: str
#     checkout_date: str
#     total_amount: int
#     payment_method: str
#
# @dataclass()
# class GetDestinationDTO:
#     destination_name: str


