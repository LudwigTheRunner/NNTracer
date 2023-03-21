
class CustomizedItem:
    def __init__(self, item, serializer, deserializer):
        self._item = item
        self._serializer = serializer
        self._deserializer = deserializer
        #TODO: Type Check for serializer and deserializer    
    
    def __serialize(self):
        self._serializer(self._item)
    
    def __deserialize(self):
        self._deserializer(self._item)

