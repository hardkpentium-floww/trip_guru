from collections import defaultdict

from graphql_service.dataloaders import BaseDataLoader
from typing import List

from trip.interactors.get_hotels_interactor import GetHotelsInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.hotel.types.types import Hotel


class DestinationHotelsLoader(BaseDataLoader):
    context_key = "get_hotels_for_destination"
    async def batch_load(self, keys: List[int]):
        storage = StorageImplementation()
        interactor = GetHotelsInteractor(storage=storage)

        hotel_dtos =  interactor.get_hotels(destination_ids=keys)

        hotels = [
            Hotel(
                id=hotel_dto.id,
                name=hotel_dto.name,
                description=hotel_dto.description,
                tariff=hotel_dto.tariff,
                image_urls=hotel_dto.image_urls,
                destination_id=hotel_dto.destination_id
            )
            for hotel_dto in hotel_dtos
        ]


        hotels_for_destination = defaultdict(list)

        for hotel in hotels:
            hotels_for_destination[hotel.destination_id].append(hotel)

        return [hotels_for_destination[key] for key in keys]

