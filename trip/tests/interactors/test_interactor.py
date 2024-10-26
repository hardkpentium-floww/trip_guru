import json
from unittest.mock import create_autospec
import pytest

from trip.interactors.login_interactor import LoginInteractor
from trip.interactors.storage_interfaces.storage_interface import StorageInterface

pytestmark = pytest.mark.django_db


class TestInteractor:
    @pytest.fixture
    def storage(self):
        storage = create_autospec(StorageInterface)
        return storage


    @pytest.fixture
    def interactor(self, storage):
        interactor = LoginInteractor(storage=storage)
        return interactor


    def test_login(self, interactor, storage):
        pass
