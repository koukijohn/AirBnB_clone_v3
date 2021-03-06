#!/usr/bin/python3
'''
    This module contains our helper functions for FileStorage and DBStorage.
'''
import models
import os

def convert_class(cls, choice="string"):
    '''
        This will convert our cls to a string in case it's not.
        Or it will return None.
    '''
    if choice == 'string':
        if cls is None or cls == "":
            c = None
        elif type(cls) != str:
            c = cls.__classname__
        else:
            c = cls
        return c
    elif choice == 'class':
        c = convert_class(cls, 'string')
        return (models.classes.get(c))

def load_test_data(choice="file", overwrite=True):
    '''
        This will load test data.
    '''

    if overwrite:
        getall = models.storage.all().copy()
        for ele in getall.values():
            models.storage.delete(ele)

    states = ['Alabama', 'Arizona', 'Washington', 'Texas', 'California']
    cities = ['One', 'Two', 'Three']

    if choice == "file":
        fs = models.storage
        for x in states:
            new_state = models.State()
            setattr(new_state, "name", x)
            fs.new(new_state)
        fs.save()

        model_states = fs.all("State")
        for x in model_states.values():
            for v in cities:
                new_city = models.City()
                setattr(new_city, "state_id", x.id)
                setattr(new_city, "name", v)
                fs.new(new_city)
        fs.save()
    else:
        pass
