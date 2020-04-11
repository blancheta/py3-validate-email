from unittest.case import TestCase

from validate_email.domainlist_check import (
    domainlist_check, update_builtin_blacklist)
from validate_email.exceptions import DomainBlacklistedError
from validate_email.validate_email import (
    validate_email, validate_email_or_fail)


class BlacklistCheckTestCase(TestCase):
    'Testing if the included blacklist filtering works.'

    def setUpClass():
        update_builtin_blacklist(force=False, background=False)

    def test_blacklist_positive(self):
        'Disallows blacklist item: mailinator.com.'
        with self.assertRaises(DomainBlacklistedError):
            domainlist_check(user_part='pa2', domain_part='mailinator.com')
        with self.assertRaises(DomainBlacklistedError):
            validate_email_or_fail(
                email_address='pa2@mailinator.com', check_regex=False,
                use_blacklist=True)
        with self.assertRaises(DomainBlacklistedError):
            validate_email_or_fail(
                email_address='pa2@mailinator.com', check_regex=True,
                use_blacklist=True)
        with self.assertLogs():
            self.assertFalse(expr=validate_email(
                email_address='pa2@mailinator.com', check_regex=False,
                use_blacklist=True))
        with self.assertLogs():
            self.assertFalse(expr=validate_email(
                email_address='pa2@mailinator.com', check_regex=True,
                use_blacklist=True))

    def test_blacklist_negative(self):
        'Allows a domain not in the blacklist.'
        self.assertTrue(expr=domainlist_check(
            user_part='pa2',
            domain_part='some-random-domain-thats-not-blacklisted.com'))
