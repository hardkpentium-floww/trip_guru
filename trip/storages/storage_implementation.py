from ib_users.models import UserAccount
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken, RefreshToken
from trip.exceptions.custom_exceptions import InvalidBooking, InvalidAdminUser, InvalidDestination, \
    BookingScheduleOverlap
from trip.interactors.storage_interfaces.storage_interface import DestinationDTO, GetDestinationsDTO, HotelDTO, \
    RatingDTO, BookingDTO, StorageInterface, UpdateBookingDTO, MutateDestinationDTO, MutateHotelDTO, MutateRatingDTO, \
    MutateBookingDTO, SearchDestinationDTO, AccessTokenDTO, RefreshTokenDTO
from typing import List
from django.db.models import Q
from trip.models import Destination, Hotel, Rating, Booking,User
from trip.exceptions.custom_exceptions import InvalidUser


class StorageImplementation(StorageInterface):
    def add_destination(self, add_destination_dto: MutateDestinationDTO)->DestinationDTO :
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
            user_id = destination_obj.user_id
        )

        return destination_dto

    def search_destination(self, search_destination_dto: SearchDestinationDTO)-> List[DestinationDTO]:

        query = Q()
        if search_destination_dto.name:
            query |= Q(name__contains=search_destination_dto.name)

        if search_destination_dto.tag:
            query |= Q(tags__contains=search_destination_dto.tag)

        destination_objs = Destination.objects.filter(query).all()

        return [
            DestinationDTO(
                id=destinationObj.id,
                name=destinationObj.name,
                description=destinationObj.description,
                tags=destinationObj.tags,
                user_id = destinationObj.user_id
            ) for destinationObj in destination_objs]

    def validate_admin_user(self, user_id: str):
        check = user_id == 'e9ab68e1-95c2-41bc-966d-615a9cfd175d'
        if check:
            raise InvalidAdminUser

    def validate_destination_id(self, destination_id: int):
        check = Destination.objects.filter(id = destination_id).exists()
        if not check:
            raise InvalidDestination

    def validate_user_id(self, user_id:str):
        user = User.objects.filter(id=user_id).exists()
        if not user:
            raise InvalidUser

    def logout(self, user_id: int):

        application = Application.objects.get(name='trip_guru')
        access_token = AccessToken.objects.get(user_id=user_id, application=application)

        access_token.delete()

        return

    def get_user_account(self, user_id: str) -> UserAccount:
        user = UserAccount.objects.get(user_id=user_id)
        return user

    def create_access_token(self,
                            access_token_dto: AccessTokenDTO):

        token = access_token_dto.token
        user_id = access_token_dto.user_id
        application_name = access_token_dto.application_name
        expires = access_token_dto.expires
        source_refresh_token = access_token_dto.source_refresh_token

        user = self.get_user_account(user_id=user_id)
        application = self.get_application_instance(application_name=application_name)

        access_token = AccessToken.objects.create(
            user=user,
            token=token,
            application=application,
            expires=expires,
            scope='read write'
        )

        return access_token

    def create_refresh_token(self,
            refresh_token_dto: RefreshTokenDTO):
        token = refresh_token_dto.token
        user_id = refresh_token_dto.user_id
        application_name = refresh_token_dto.application_name
        access_token_id = refresh_token_dto.access_token_id

        application_id = self.get_application_instance(application_name=application_name).id
        refresh_token = RefreshToken.objects.create(
            user_id=user_id,
            token=token,
            application_id=application_id,
            access_token_id=access_token_id

        )

        return refresh_token

    def get_application_instance(self, application_name:str) -> Application:
        application = Application.objects.filter(name=application_name).first()
        return application

    def get_destination(self, destination_id: int)->DestinationDTO:
        destinationObj = Destination.objects.filter(
            id = destination_id).first()
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
        check = Destination.objects.filter(destination_id = destination_id, user_id = user_id).exists()

        if not check:
            raise InvalidUser

    def add_hotel(self, user_id:str, add_hotel_dto: MutateHotelDTO):

        check = Destination.objects.filter(id=add_hotel_dto.destination_id).exists()

        if not check:
            raise InvalidDestination


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

    def add_rating(self, add_rating_dto: MutateRatingDTO):

        check = Destination.objects.filter(id=add_rating_dto.destination_id).exists()

        if check:
            return InvalidDestination

        rating_obj = Rating.objects.create(
            rating = add_rating_dto.rating,
            user_id = add_rating_dto.user_id,
            review = add_rating_dto.review,
            destination_id = add_rating_dto.destination_id
        )

        rating_dto = RatingDTO(
            rating = rating_obj.rating,
            user_id = rating_obj.user_id,
            review = rating_obj.review,
            destination_id = rating_obj.destination_id
        )

        return rating_dto

    def book_hotel(self,hotel_id: int, book_hotel_dto: MutateBookingDTO):
        checkin_date = book_hotel_dto.checkin_date
        checkout_date = book_hotel_dto.checkout_date
        user_id = book_hotel_dto.user_id

        # checks in gql
        check = Destination.objects.filter(id=book_hotel_dto.destination_id).exists()

        if check:
            return InvalidDestination



        overlapping_bookings = Booking.objects.filter(
            Q(user_id=user_id) & (
                    Q(checkin_date__lt=checkout_date) &
                    Q(checkout_date__gt=checkin_date)
            )
        )

        if overlapping_bookings.exists():
            raise BookingScheduleOverlap



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

    def update_booking(self, booking_id: int, update_booking_dto: UpdateBookingDTO)->BookingDTO:
        checkin_date = update_booking_dto.checkin_date
        checkout_date = update_booking_dto.checkout_date

        overlapping_bookings = Booking.objects.filter(
            Q(id=booking_id) & (
                    Q(checkin_date__lt=checkout_date) &
                    Q(checkout_date__gt=checkin_date)
            )
        )

        if overlapping_bookings.exists():
            raise InvalidBooking

        booking = Booking.objects.get(id=update_booking_dto.booking_id)

        if checkin_date:
            booking.checkin_date = checkin_date

        if checkout_date:
            booking.checkout_date = checkout_date

        booking.save()

        booking_dto = BookingDTO(
            user_id=booking.user_id,
            hotel_id=booking.hotel_id,
            checkin_date=booking.checkin_date,
            checkout_date=booking.checkout_date,
            total_amount=booking.total_amount,
            booking_id=booking.id
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
            tags=destinationObj.tags
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
            hotel_id=hotelObj.id,
            destination_id=hotelObj.destination_id,
            name=hotelObj.name,
            description=hotelObj.description,
            tariff=hotelObj.tariff,
            image_urls=hotelObj.image_urls
        )

        return hotel_dto

    def get_hotels(self, destination_id: int)->List[HotelDTO]:
        check = Destination.objects.filter(id=destination_id).exists()
        if not check:
            raise InvalidDestination

        hotel_objs = Hotel.objects.filter(
            destination_id = destination_id
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