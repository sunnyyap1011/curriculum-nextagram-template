from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw


class Donation(BaseModel):
    amount = pw.DecimalField(decimal_places=2)
    txs_id = pw.CharField(null=True)
    donor = pw.ForeignKeyField(User, backref='donations')
    image = pw.ForeignKeyField(Image, backref='donations')
