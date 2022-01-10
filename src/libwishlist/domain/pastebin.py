from libutil import util
from libwishlist import ctx
from jsql import sql
import secrets
import pydantic


class UploadPastebin(util.NoonBaseModel):
    txt: str

    @pydantic.validator('txt')
    def must_less_than_1000_char(cls, txt):
        if len(txt) > 1000:
            raise ValueError('must be less than 1000 characters')
        return txt

    def execute(self):
        assert self.txt != 'illegal content', 'cant store illegal content'

        code = secrets.token_hex(16)
        sql(
            ctx.conn,
            '''
            INSERT INTO pastebin (code, txt)
            VALUES (:code, :txt)
        ''',
            code=code,
            **self.dict(),
        )
        return code


def get_pastebin(pastebin_code):
    return sql(
        ctx.conn, 'SELECT id_pastebin, txt FROM pastebin WHERE code=:pastebin_code', pastebin_code=pastebin_code
    ).dict()

