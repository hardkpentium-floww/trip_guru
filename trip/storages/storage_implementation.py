from datetime import datetime
from typing import List

from django.db.models import Q

from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidDestination, \
    BookingScheduleOverlap, NoBookingsExists, InvalidHotel, InvalidCheckinCheckoutDate, InvalidRating, InvalidTariff
from trip.exceptions.custom_exceptions import InvalidUser
from trip.interactors.storage_interfaces.storage_interface import DestinationDTO, GetDestinationsDTO, HotelDTO, \
    RatingDTO, BookingDTO, StorageInterface, MutateDestinationDTO, MutateHotelDTO, \
    MutateBookingDTO, AccessTokenDTO, RefreshTokenDTO, AddRatingDTO, AddDestinationDTO, AddHotelDTO, AddBookingDTO
from trip.models import Destination, Hotel, Rating, Booking


class StorageImplementation(StorageInterface):

    def add_destination(self, add_destination_dto: AddDestinationDTO)->DestinationDTO :
        destination_obj = Destination.objects.create(
            name = add_destination_dto.name,
            description = add_destination_dto.description,
            tags = add_destination_dto.tags,
            user_id = add_destination_dto.user_id

        )
        destination_dto = DestinationDTO(
            id = destination_obj.id,
            name = destination_obj.name,
            description = destination_obj.description,
            tags = destination_obj.tags,
            user_id = destination_obj.user_id,
        )

        return destination_dto

    def add_hotels(self, user_id: str, add_hotel_dtos: List[AddHotelDTO], destination_id: int):

        hotel_objs =[Hotel(
            name = hotel_dto.name,
            description = hotel_dto.description,
            image_urls = hotel_dto.image_urls,
            tariff = hotel_dto.tariff,
            destination_id = destination_id
        ) for hotel_dto in add_hotel_dtos]

        Hotel.objects.bulk_create(hotel_objs)

        hotel_dtos = [HotelDTO(
            id = hotel_obj.id,
            name = hotel_obj.name,
            description=hotel_obj.description,
            image_urls=hotel_obj.image_urls,
            tariff=hotel_obj.tariff,
            destination_id=destination_id
        ) for hotel_obj in hotel_objs]

        return hotel_dtos

    def check_duplicate_destination(self, add_destination_dto):
        check = Destination.objects.filter(name=add_destination_dto.name).exists()
        return check

    def check_duplicate_hotels(self, add_hotel_dtos: List[AddHotelDTO]):

        names = [add_hotel_dto.name for add_hotel_dto in add_hotel_dtos]
        names_set = set(names)

        if len(names) != len(names_set):
            raise InvalidHotel

        check = Hotel.objects.filter(name__in=names).exists()

        return check

    def validate_checkin_checkout_date(self, checkin_date: datetime, checkout_date: datetime):
        check = (checkin_date < checkout_date)
        return check

    def validate_admin_user(self, user_id: str):
        check = (str(user_id) == "test_user")
        return check

    def validate_destination_id(self, destination_id: int):
        check = Destination.objects.filter(id = destination_id).exists()
        return check

    def validate_user_id(self, user_id:str):
        from ib_users.models import UserAccount
        check_user = UserAccount.objects.filter(user_id=user_id).exists()
        return check_user

    def logout(self, user_id: str, access_token:str):
        from oauth2_provider.models import AccessToken

        access_tokens = AccessToken.objects.filter(token=access_token, user_id=user_id)

        for access_token in access_tokens:
            access_token.expires = datetime.now()
            access_token.save()


    def get_user_account(self, user_id: str):
        from ib_users.models import UserAccount
        user = UserAccount.objects.filter(user_id=user_id)
        if user.exists():
            return user[0]



    def create_access_token(self,
                            access_token_dto: AccessTokenDTO):
        from oauth2_provider.models import AccessToken

        token = access_token_dto.token
        user_id = access_token_dto.user_id
        application_name = access_token_dto.application_name
        expires = access_token_dto.expires
        source_refresh_token = access_token_dto.source_refresh_token

        application = self.get_application_instance(application_name=application_name)

        access_token = AccessToken.objects.create(
            user_id=user_id,
            token=token,
            application=application,
            expires=expires,
            scope='read write'
        )

        return access_token

    def create_refresh_token(self,
            refresh_token_dto: RefreshTokenDTO):
        from oauth2_provider.models import RefreshToken,AccessToken
        token = refresh_token_dto.token
        user_id = refresh_token_dto.user_id
        application_name = refresh_token_dto.application_name
        access_token_id = refresh_token_dto.access_token_id
        application_id = self.get_application_id(application_name=application_name)

        refresh_token = RefreshToken.objects.create(
            user_id=user_id,
            token=token,
            application_id=application_id,
            access_token_id=access_token_id

        )

        return refresh_token

    def get_application_id(self, application_name:str):
        from oauth2_provider.models import Application
        application = Application.objects.filter(name=application_name).values('id').first()
        return application['id']

    def get_application_instance(self, application_name:str):
        from oauth2_provider.models import Application

        application = Application.objects.filter(name=application_name).first()
        return application

    def get_destination(self, destination_id: int)->DestinationDTO:
        destinationObj = Destination.objects.get(
            id = destination_id)
        destination_dto = DestinationDTO(
            id = destinationObj.id,
            name=destinationObj.name,
            description=destinationObj.description,
            tags=destinationObj.tags,
            user_id = destinationObj.user_id
        )

        return destination_dto

    def get_destinations(self, get_destinations_dto: GetDestinationsDTO)-> List[DestinationDTO]:
        destination_objs = Destination.objects.filter(
            tags__contains = get_destinations_dto.tag
        ).all()
        offset = get_destinations_dto.offset
        limit = get_destinations_dto.limit

        destination_objs = destination_objs[offset:offset+limit]

        return [
            DestinationDTO(
                id=destinationObj.id,
                name=destinationObj.name,
                description=destinationObj.description,
                tags=destinationObj.tags,
                user_id=destinationObj.user_id
            ) for destinationObj in destination_objs]

    def validate_hotel_customer(self,destination_id: int, user_id: str):
        check = Destination.objects.filter(id = destination_id, user_id = user_id).exists()

        return check

    def add_hotel(self, user_id:str, add_hotel_dto: AddHotelDTO):

        hotel_obj = Hotel.objects.create(
            name = add_hotel_dto.name,
            description = add_hotel_dto.description,
            tariff = add_hotel_dto.tariff,
            image_urls = add_hotel_dto.image_urls,
            destination_id = add_hotel_dto.destination_id
        )

        hotel_dto = HotelDTO(
            id = hotel_obj.id,
            name = hotel_obj.name,
            description = hotel_obj.description,
            tariff = hotel_obj.tariff,
            image_urls = hotel_obj.image_urls,
            destination_id = hotel_obj.destination_id

        )

        return hotel_dto

    def validate_hotel_id(self, hotel_id: int):
        check = Hotel.objects.filter(id = hotel_id).exists()
        return check

    def get_hotel(self, hotel_id: int)->HotelDTO:

        hotel_obj = Hotel.objects.filter(
            id = hotel_id
        ).first()


        hotel_dto = HotelDTO(
            id = hotel_obj.id,
            name = hotel_obj.name,
            description = hotel_obj.description,
            tariff = hotel_obj.tariff,
            image_urls = hotel_obj.image_urls,
            destination_id = hotel_obj.destination_id
        )

        return hotel_dto

    def add_rating(self, add_rating_dto: AddRatingDTO):

        rating_obj = Rating.objects.create(
            rating = add_rating_dto.rating,
            user_id = add_rating_dto.user_id,
            review = add_rating_dto.review,
            destination_id = add_rating_dto.destination_id
        )

        rating_dto = RatingDTO(
            id = rating_obj.id,
            rating = rating_obj.rating,
            user_id = rating_obj.user_id,
            review = rating_obj.review,
            destination_id = rating_obj.destination_id
        )

        return rating_dto

    def check_overlapping_bookings(self, user_id: str, checkin_date:datetime, checkout_date:datetime):

        overlapping_bookings = Booking.objects.filter(
            Q(user_id=user_id) & (
                    Q(checkin_date__lt=checkout_date) &
                    Q(checkout_date__gt=checkin_date)
            )
        )

        return overlapping_bookings.exists()




    def book_hotel(self,hotel_id: int, book_hotel_dto: AddBookingDTO):
        checkin_date = book_hotel_dto.checkin_date
        checkout_date = book_hotel_dto.checkout_date
        user_id = book_hotel_dto.user_id

        booking_obj = Booking.objects.create(
            user_id = book_hotel_dto.user_id,
            hotel_id = hotel_id,
            checkin_date = book_hotel_dto.checkin_date,
            checkout_date = book_hotel_dto.checkout_date,
            tariff = book_hotel_dto.total_amount,
            destination_id = book_hotel_dto.destination_id,
            total_amount = book_hotel_dto.total_amount
        )

        booking_dto = BookingDTO(
            user_id = booking_obj.user_id,
            hotel_id = booking_obj.hotel_id,
            checkin_date = booking_obj.checkin_date,
            checkout_date = booking_obj.checkout_date,
            total_amount = booking_obj.total_amount,
            booking_id=booking_obj.id,
            destination_id = booking_obj.destination_id
        )

        return booking_dto

    def update_booking(self, booking_id: int, update_booking_dto: MutateBookingDTO)->BookingDTO:
        checkin_date = update_booking_dto.checkin_date
        checkout_date = update_booking_dto.checkout_date
        booking = Booking.objects.get(id=booking_id)

        if checkin_date:
            booking.checkin_date = checkin_date

        if checkout_date:
            booking.checkout_date = checkout_date

        booking.total_amount = update_booking_dto.total_amount

        booking.save()

        booking_dto = BookingDTO(
            user_id=booking.user_id,
            hotel_id=booking.hotel_id,
            checkin_date=booking.checkin_date,
            checkout_date=booking.checkout_date,
            total_amount=booking.total_amount,
            booking_id=booking.id,
            destination_id=booking.destination_id
        )

        return booking_dto



    def update_destination(self, destination_id: int, update_destination_dto: MutateDestinationDTO)->DestinationDTO:

        destinationObj = Destination.objects.get(id=destination_id)

        if update_destination_dto.name:
            destinationObj.name = update_destination_dto.name

        if update_destination_dto.description:
            destinationObj.description = update_destination_dto.description

        if update_destination_dto.tags:
            destinationObj.tags = update_destination_dto.tags

        destinationObj.save()

        destination_dto = DestinationDTO(
            id=destinationObj.id,
            name=destinationObj.name,
            description=destinationObj.description,
            tags=destinationObj.tags,
            user_id = destinationObj.user_id
        )

        return destination_dto

    def update_hotel(self,hotel_id: int, update_hotel_dto: MutateHotelDTO)->HotelDTO:

        hotelObj = Hotel.objects.get(id=hotel_id)

        if update_hotel_dto.name:
            hotelObj.name = update_hotel_dto.name

        if update_hotel_dto.description:
            hotelObj.description = update_hotel_dto.description

        if update_hotel_dto.tariff:
            hotelObj.tariff = update_hotel_dto.tariff

        if update_hotel_dto.image_urls:
            hotelObj.image_urls = update_hotel_dto.image_urls

        hotelObj.save()

        hotel_dto = HotelDTO(
            id=hotelObj.id,
            destination_id=hotelObj.destination_id,
            name=hotelObj.name,
            description=hotelObj.description,
            tariff=hotelObj.tariff,
            image_urls=hotelObj.image_urls
        )

        return hotel_dto

    def get_bookings_for_user(self, user_id: int, offset: int, limit: int) -> List[BookingDTO]:
        check = Booking.objects.filter(user_id=user_id).exists()
        if not check:
            raise NoBookingsExists

        booking_objs = Booking.objects.filter(user_id=user_id).all()

        return [
            BookingDTO(
                booking_id = booking_obj.id,
                user_id = booking_obj.user_id,
                hotel_id = booking_obj.hotel_id,
                checkin_date = booking_obj.checkin_date,
                checkout_date = booking_obj.checkout_date,
                total_amount = booking_obj.total_amount,
                destination_id = booking_obj.destination_id
            ) for booking_obj in booking_objs
        ]

    def get_hotels(self, destination_ids: List[int])->List[HotelDTO]:
        destination_check = Destination.objects.filter(id__in=destination_ids).exists()
        if not destination_check:
            raise InvalidDestination

        hotel_objs = Hotel.objects.filter(
            destination_id__in = destination_ids
        ).all()

        return [
            HotelDTO(
                id = hotel_obj.id,
                name = hotel_obj.name,
                description = hotel_obj.description,
                tariff = hotel_obj.tariff,
                image_urls = hotel_obj.image_urls,
                destination_id = hotel_obj.destination_id
            ) for hotel_obj in hotel_objs
        ]