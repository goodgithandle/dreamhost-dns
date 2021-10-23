'''
dreamhost_dns

A python package to work with Dreamhost DNS Records using the Dreamhost API.
'''
from funcs import DNSRecord
from funcs import list_all_records
from funcs import update_record_to_public_ip

__all__ = ['DNSRecord', 'list_all_records', 'update_record_to_public_ip']