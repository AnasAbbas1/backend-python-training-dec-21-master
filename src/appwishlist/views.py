import logging

from fastapi import APIRouter

from libwishlist import Context, domain
from libutil import util
from noonutil.v1 import fastapiutil

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post('/pastebin/create', summary='create pastebin', tags=['pastebin'])
def create_pastebin(msg: domain.pastebin.UploadPastebin):
    with Context.fastapi():
        return {"pastebin_code": msg.execute()}


@router.post('/wishlist/create', summary = 'create a wishlist',tags = ['wishlist'])
def create_wishlist(msg: domain.wishlist.CreateWishlist):
        with Context.fastapi():
            return {"wishlist_nr": msg.execute()}

@router.get('/wishlist/{wishlist_nr}', summary = 'get a specific wishlist',tags = ['wishlist'])
def get_wishlist(wishlist_nr):
        with Context.fastapi():
            return {"wishlist_nr": domain.wishlist.Wishlist(wishlist_nr = wishlist_nr).detail()}


@router.post('/wishlist/{name}', summary = 'delete a specific wishlist',tags = ['wishlist'])
def delete_wishlist(name):
        with Context.fastapi():
            return {domain.wishlist.Wishlist(name = name).delete()}