# -*- coding: utf-8 -*-
from twisted.internet import defer

from synapse.api.errors import SynapseError, AuthError

from ._base import BaseHandler


class ProfileHandler(BaseHandler):

    def __init__(self, hs):
        super(ProfileHandler, self).__init__(hs)

        distributor = hs.get_distributor()
        distributor.observe("registered_user", self.registered_user)

    def registered_user(self, user):
        self.store.create_profile(user.localpart)

    @defer.inlineCallbacks
    def get_displayname(self, target_user):
        if target_user.is_mine:
            displayname = yield self.store.get_profile_displayname(
                    target_user.localpart)

            defer.returnValue(displayname)
        else:
            # TODO(paul): This should use the server-server API to ask another
            # HS
            defer.returnValue("Bob")

    @defer.inlineCallbacks
    def set_displayname(self, target_user, auth_user,
            new_displayname):
        """target_user is the user whose displayname is to be changed;
        auth_user is the user attempting to make this change."""
        if not target_user.is_mine:
            raise SynapseError(400, "User is not hosted on this Home Server")

        if target_user != auth_user:
            raise AuthError(400, "Cannot set another user's displayname")

        yield self.store.set_profile_displayname(target_user.localpart,
                new_displayname)

    @defer.inlineCallbacks
    def get_avatar_url(self, target_user):
        if target_user.is_mine:
            avatar_url = yield self.store.get_profile_avatar_url(
                    target_user.localpart)

            defer.returnValue(avatar_url)
        else:
            # TODO(paul): This should use the server-server API to ask another
            # HS
            defer.returnValue("http://elsewhere/")

    @defer.inlineCallbacks
    def set_avatar_url(self, target_user, auth_user,
            new_avatar_url):
        """target_user is the user whose avatar_url is to be changed;
        auth_user is the user attempting to make this change."""
        if not target_user.is_mine:
            raise SynapseError(400, "User is not hosted on this Home Server")

        if target_user != auth_user:
            raise AuthError(400, "Cannot set another user's avatar_url")

        yield self.store.set_profile_avatar_url(target_user.localpart,
                new_avatar_url)
