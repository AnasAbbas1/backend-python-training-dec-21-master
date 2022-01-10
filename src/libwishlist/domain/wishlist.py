from typing import List
from libutil import util
from libwishlist import ctx
from jsql import sql
import secrets
import pydantic
import random
import libwishlist
from noonutil.v1 import miscutil, sqlutil
from libwishlist.models import tables


class CreateWishlist(util.NoonBaseModel):

    name: str
    items: List[str]

    def execute(self):

        assert len(self.items) > 0, 'wish list cannot be empty'
        
        wishlist_nr = 'WL' + str(random.randint(1e5, 1e6 - 1)) + 'C'

        wishlist_row = {
            'wishlist_nr': wishlist_nr,
            'username': ctx.user_code,
            'name': self.name
        }

        id_wishlist = sqlutil.insert_one(ctx.conn, tables.Wishlist, wishlist_row).lastrowid;
        wishlist_item_rows = []
        for item in self.items:
            wishlist_item_rows.append({
                'id_wishlist': id_wishlist,
                'psku_code': item,
                'name': 'wishlistItemName'
            })
        sqlutil.insert_batch(ctx.conn, tables.WishlistItem, wishlist_item_rows)

        return wishlist_nr


class Wishlist(util.NoonBaseModel):

    wishlist_nr: str = ''
    name: str = ''

    def detail(self):
        wl_details =  sql(ctx.conn,'''
            select wl.name , wli.psku_code as item
            from wishlist wl
            left join wishlist_item wli using (id_wishlist)
            where wl.wishlist_nr = :wishlist_nr
            and is_active = 1
        ''',wishlist_nr = self.wishlist_nr).dicts()
        assert wl_details, "wishlist is either doesn't exist or inactive"

        return {
            'name': wl_details[0]['name'],
            'items': miscutil.pluck('item', wl_details)
        }

    def delete(self):

        sql(ctx.conn, '''update wishlist set is_active = 0 where name = :name''', name = self.name)

        return 'success'
