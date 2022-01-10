from datetime import datetime
import pytest

from libwishlist import Context, domain


def test_domain():
    with Context.service():
        pastebin_code = domain.pastebin.UploadPastebin(txt="pastebin text").execute()
        assert pastebin_code


def test_views(client):
    response = client.post(
        '/pastebin/create',
        json={
            "txt": "pastebin text 2",
        },
    )
    pastebin_code = response.json()['pastebin_code']


def test_illegal_content(client):
    response = client.post(
        '/pastebin/create',
        json={
            "txt": "illegal content",
        },
        assert_status=400,
    )

    with pytest.raises(AssertionError, match='.*cant store illegal content.*'):
        response = client.post(
            '/pastebin/create',
            json={
                "txt": "illegal content",
            },
        )
