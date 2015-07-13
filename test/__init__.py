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
Tests for the LDAP plugin.
"""

import unittest

import ldap
import mock

from ocupado_plugin_ldap import LDAP


class TestOcupadoPluginLDAP(unittest.TestCase):

    def setUp(self):
        self.l = LDAP(
            uri='ldap://127.0.0.1:1390',
            base='dc=example,dc=org',
            filter='(cn=%s)'
        )

    def test_ldap_plugin__init(self):
        self.assertEquals(self.l._uri, 'ldap://127.0.0.1:1390')
        self.assertEquals(self.l._con._uri, 'ldap://127.0.0.1:1390')
        self.assertEquals(self.l._base, 'dc=example,dc=org')
        self.assertEquals(self.l._filter, '(cn=%s)')
        self.assertEquals(self.l._user, None)
        self.assertEquals(self.l._passwd, None)

    def test_plugin_ldap_authenticate_without_user(self):
        with mock.patch('ldap.ldapobject.SimpleLDAPObject.simple_bind_s') as (
                _simple_bind_s):
            self.l.authenticate()
            self.assertEquals(_simple_bind_s.call_count, 0)

    def test_plugin_ldap_authenticate_with_user(self):
        with mock.patch('ldap.ldapobject.SimpleLDAPObject.simple_bind_s') as (
                _simple_bind_s):
            l = LDAP(
                uri='ldap://127.0.0.1:1390',
                base='dc=example,dc=org',
                filter='(cn=%s)',
                user='user',
                passwd='passwd'
            )
            l.authenticate()
            self.assertEquals(_simple_bind_s.call_count, 1)

    def test_plugin_ldap_logout(self):
        with mock.patch('ldap.ldapobject.SimpleLDAPObject.unbind_ext_s') as (
                _unbind_ext_s):
            self.l.logout()
            self.assertEquals(_unbind_ext_s.call_count, 1)

    def test_plugin_ldap_exists(self):
        with mock.patch('ldap.ldapobject.SimpleLDAPObject.search_s') as (
                _search_s):
            _search_s.return_value = [(
                'cn=userid,dc=example,dc=org', {'cn': ['userid']})]
            result = self.l.exists('userid')
            _search_s.called_once_with(
                'dc=example,dc=org', ldap.SCOPE_SUBTREE, '(cn=userid)')
            self.assertEquals(
                result,
                (True, {'exists': True, 'details': {'username': 'userid'}}))

    def test_plugin_ldap_exists_with_no_result(self):
        with mock.patch('ldap.ldapobject.SimpleLDAPObject.search_s') as (
                _search_s):
            _search_s.return_value = None
            result = self.l.exists('userid')
            _search_s.called_once_with(
                'dc=example,dc=org', ldap.SCOPE_SUBTREE, '(cn=userid)')
            self.assertEquals(
                result,
                (False, {'exists': False, 'details': {'username': 'userid'}}))
