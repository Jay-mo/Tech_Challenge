from mongoengine import Document, StringField, IntField, BooleanField


class URL(Document):
    url = StringField(required=True)
    port = IntField(required=True)
    block_status = BooleanField(required=True)

    def format(self):
        return {
            'url' : self.url,
            'port' : self.port,
            'block_status': self.block_status
        }

    
    meta = {
        'indexes': [
            
            {
                'fields': ['url', 'port'],
                'unique': True}
        ]
    }