# -*- coding: utf-8 -*-
""" This module contains REST servlets to do with profile: /profile/<paths> """
from twisted.internet import defer

from synapse.api.errors import SynapseError, cs_error

from base import RestServlet, InvalidHttpRequestError

import json
import re


class ProfileDisplaynameRestServlet(RestServlet):
    PATTERN = re.compile("^/profile/(?P<user_id>[^/]*)/displayname")

    @defer.inlineCallbacks
    def on_GET(self, request, user_id):
        user = self.hs.parse_userid(user_id)

        displayname = yield self.handlers.profile_handler.get_displayname(user)

        defer.returnValue((200, {"displayname": displayname}))

    @defer.inlineCallbacks
    def on_PUT(self, request, user_id):
        auth_user = yield self.auth.get_user_by_req(request)
        user = self.hs.parse_userid(user_id)

        try:
            content = json.loads(request.content.read())
            new_name = content["displayname"]
        except:
            defer.returnValue((400, "Unable to parse name"))

        yield self.handlers.profile_handler.set_displayname(user,
                auth_user, new_name)

        defer.returnValue((200, ""))


class ProfileAvatarURLRestServlet(RestServlet):
    PATTERN = re.compile("^/profile/(?P<user_id>[^/]*)/avatar_url")

    @defer.inlineCallbacks
    def on_GET(self, request, user_id):
        user = self.hs.parse_userid(user_id)

        avatar_url = yield self.handlers.profile_handler.get_avatar_url(user)

        defer.returnValue((200, {"avatar_url": avatar_url}))

    @defer.inlineCallbacks
    def on_PUT(self, request, user_id):
        auth_user = yield self.auth.get_user_by_req(request)
        user = self.hs.parse_userid(user_id)

        try:
            content = json.loads(request.content.read())
            new_name = content["avatar_url"]
        except:
            defer.returnValue((400, "Unable to parse name"))

        yield self.handlers.profile_handler.set_avatar_url(user,
                auth_user, new_name)

        defer.returnValue((200, ""))


def register_servlets(hs, http_server):
    ProfileDisplaynameRestServlet(hs).register(http_server)
    ProfileAvatarURLRestServlet(hs).register(http_server)
