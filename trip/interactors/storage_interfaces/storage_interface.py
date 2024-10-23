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
class HotelDTO:
    id: int
    name: str
    description: str
    tariff: int
    image_urls: str
    destination_id: int


@dataclass()
class RatingDTO:
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
    id: int
    hotel_id: int
    user_id: str
    destination_id: int
    checkin_date: str
    checkout_date: str
    total_amount: int

@dataclass()
class GetDestinationsDTO:
  offset = int
  limit = int
  tag = str


@dataclass()
class UpdateBookingDTO:
    booking_id: int
    user_id: str
    checkin_date: str
    checkout_date: str

class StorageInterface:
    def add_destination(self, add_destination_dto: DestinationDTO)->DestinationDTO :
        pass

    def validate_admin_user(self, user_id: str):
        pass

    def get_destination(self, destination_id: int)->DestinationDTO:
        pass

    def get_destinations(self, get_destination_dto: GetDestinationsDTO)-> List[DestinationDTO]:
        pass

    def add_hotel(self, add_hotel_dto: HotelDTO):
        pass

    def get_hotel(self, hotel_id: int)->HotelDTO    :
        pass

    def add_rating(self, add_rating_dto: RatingDTO):
        pass

    def book_hotel(self, book_hotel_dto: BookingDTO):
        pass

    def update_booking(self, update_booking_dto: UpdateBookingDTO)->BookingDTO:
        pass

    def update_destination(self, update_destination_dto: DestinationDTO)->DestinationDTO:
        pass

    def update_hotel(self, update_hotel_dto: HotelDTO)->HotelDTO:
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


