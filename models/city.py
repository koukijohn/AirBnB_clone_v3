#!/usr/bin/python3
'''
    Define the class City.
'''
from os import getenv
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.state import State


class City(BaseModel, Base):
    '''
        Define the class City that inherits from BaseModel.
    '''
    __tablename__ = "cities"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete, delete-orphan")
    else:
        state_id = ""
        name = ""

        @property
        def places():
            '''
                This will return all places belonging to the City.
            '''
            empty_list = []
            all_places = models.storage.all("Place")
            for place in all_places:
                if place.city_id == self.id:
                    empty_list.append(place)
            return empty_list
