import json
import tweepy
import re

from .base_operator import BaseOperator

from ai_context import AiContext


class PersistVectorIndex(BaseOperator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def declare_name():
        return 'Persist Vector Index'

    @staticmethod
    def declare_parameters():
        return [
            {
                # Optional, will overwrite existing index if present.
                # Must check for ownership so that other users cannot nuke index created by somebody else.
                "name": "index_id",
                "data_type": "string",
            }
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "vector_index",
                # Just a dictionary, without specifying any keys that are expected to be present there.
                # Naturally since it is vector index, the keys are going to be str(embedding vector).
                "data_type": "{}",
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "index_id",
                "data_type": "string",
            }
        ]
        

    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        vi_uuid = step['parameters'].get('index_id')
        vector_index = ai_context.get_input('vector_index', self)
        
        print(f'type(vector_index) = {type(vector_index)}, vector_index = {vector_index}')
        
        vi_uuid = ai_context.publish_vector_index(vector_index, vi_uuid=vi_uuid)
        ai_context.set_output('index_id', vi_uuid, self)
    
        ai_context.add_to_log(
            f'Vector Index created: {vi_uuid}. Put this id to ChatBot operator to create chat'
            ' bot that would query the index and also store user specific history', 
            color='blue'
        )
         

