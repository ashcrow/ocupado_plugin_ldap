# Copyright (C) 2015 SEE AUTHORS FILE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
LDAP plugin for the ocupado tool.
"""


import ldap

from ldap.filter import escape_filter_chars

from ocupado.plugin import Plugin

__version__ = '0.0.1'


class LDAP:
    """
    LDAP plugin for ocupado.
    """

    def __init__(self, uri, base, filter, user=None, passwd=None):
        """
        Creates an instance of the LDAP plugin.

        :uri: The ldap connection uri string
        :base: The search base to use. EX: ou=testing,dc=example,dc=org
        :filter: Filter to use when searching: EX: (cn=%s)
        :user: Optional user to pass if authentication is required
        :passwd: Optional password to pass if authentication is required
        """
        self._uri = uri
        self._con = ldap.initialize(self._uri)
        self._base = base
        self._filter = filter
        self._user = user
        self._passwd = passwd

    def authenticate(self):
        """
        Defines how to authenticate via LDAP.
        """
        if self._user and self._passwd:
            self._con.simple_bind_s(self._user, self._passwd)
            self._user = None
            self._passwd = None

    def logout(self):
        """
        Defines how to logout via a Plugin.
        """
        self._con.unbind_s()

    def exists(self, userid):
        """
        Checks for the existance of a user in LDAP.

        :userid: The userid to check.
        """
        safe_filter = self._filter % escape_filter_chars(userid)
        result = self._con.search_s(
            self._base, ldap.SCOPE_ONELEVEL, safe_filter)
        if result == [] or result is None:
            return False, {'exists': False, 'details': {'username': userid}}
        return True, {"exists": True, "details": {"username": userid}}

    def get_all_usernames(self):
        """
        Returns **all** user names.
        """
        # TODO
        raise NotImplementedError('get_all_users() must be implemented')
