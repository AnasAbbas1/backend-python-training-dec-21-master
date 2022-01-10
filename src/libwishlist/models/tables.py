from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, types
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import UniqueConstraint, Index
import sqlalchemy as sa

import libwishlist


def create_all():
    Base.metadata.create_all(libwishlist.engine)


def recreate_all():
    import os

    assert os.getenv('ENV') == 'dev', 'must be dev'
    assert libwishlist.engine.url.username == 'root'
    assert libwishlist.engine.url.password == 'root'
    Base.metadata.drop_all(libwishlist.engine)
    Base.metadata.create_all(libwishlist.engine)


Base = declarative_base()


class Model(Base):
    __abstract__ = True
    __bind_key__ = 'wishlist'


TINYINT = mysql.TINYINT(unsigned=True)
SMALLINT = mysql.SMALLINT(unsigned=True)
MEDIUMINT = mysql.MEDIUMINT(unsigned=True)
INT = mysql.INTEGER(unsigned=True)
BIGINT = mysql.BIGINT(unsigned=True)
SINT = mysql.INTEGER(unsigned=False)
SBIGINT = mysql.BIGINT(unsigned=False)
CCY = sa.Numeric(13, 2)


class Pastebin(Model):
    __tablename__ = 'pastebin'
    id_pastebin = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.String(50), nullable=False, unique=True)
    txt = sa.Column(sa.String(1000), nullable=False)
    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = sa.Column(
        types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False
    )

class Wishlist(Model):
    __tablename__ = 'wishlist'
    id_wishlist = sa.Column(sa.Integer, primary_key=True)
    wishlist_nr = sa.Column(sa.String(25), nullable=False, unique=True)
    username = sa.Column(sa.String(25), nullable=False)
    name = sa.Column(sa.String(100), nullable=False)
    is_active = sa.Column(sa.Boolean, nullable=False, server_default='1')

    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = sa.Column(
        types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False
    )

class WishlistItem(Model):
    __tablename__ = 'wishlist_item'
    id_wishlist_item = sa.Column(sa.Integer, primary_key=True)
    id_wishlist = sa.Column(sa.Integer, nullable=False)
    psku_code = sa.Column(sa.String(100), nullable=False)
    name = sa.Column(sa.String(100), nullable=False)

    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = sa.Column(
        types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False
    )

    __table_args = (UniqueConstraint('id_wishlist', 'psku_code', name= 'uq_wishlist_psku'))