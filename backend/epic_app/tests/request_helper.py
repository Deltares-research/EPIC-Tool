from wsgiref.simple_server import WSGIRequestHandler

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory


def _fill_in_request(request: WSGIRequestHandler) -> WSGIRequestHandler:
    # adding session
    middleware = SessionMiddleware(request)
    middleware.process_request(request)
    request.session.save()

    # adding messages
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    return request


def _create_get_request(get_url: str) -> WSGIRequestHandler:
    return _fill_in_request(RequestFactory().get(get_url))


def _create_post_request(post_url: str) -> WSGIRequestHandler:
    return _fill_in_request(RequestFactory().post(post_url))
