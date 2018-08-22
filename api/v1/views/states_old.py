#!/usr/bin/python3
'''
'''
import models

class State:

    def __init__(self):
        self.ret = {}
        self.reload()

    def reload(self):
        '''
            Reloads dict
        '''
        self.all_states = models.storage.all("State")
        for v in self.all_state.values():
            self.ret[v.id] = v.to_dict()

    def get_method(self, id):
        '''
        '''
        return self.ret.get(id)

    def post_method(body):
        '''
        '''
        if body.get("name") is None:
            return None
        state = models.classes["State"]()
        for k, v in body.items():
            setattr(state, k, v)
        models.storage.new(state)
        models.storage.save()
        return state.to_dict()


    def put_method(id, body):
        '''
        '''
        exists = self.ret.get(id)
        if exists:
            for k, v in body.items():
                setattr(exists, k, v)
            models.storage.save()
            return exists
        else:
            return None
