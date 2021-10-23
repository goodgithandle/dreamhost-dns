from requests import get
import configparser
import os
from typing import List

this_dir = os.path.dirname(os.path.realpath(__name__))
config = configparser.ConfigParser()
config.read(os.path.join(this_dir, 'settings.ini'))

API_TOKEN = config['DREAMHOST']['token']
DOMAIN = config['DREAMHOST']['domain']


class DNSRecord():
    '''
    A Dreamhost DNS record

    :param account_id: The Dreamhost Account ID
    :type account_id: int
    :param value: The Dreamhost DNS Record's value
    :type value: str
    :param record_type: The Dreamhost DNS Record's type (eg. 'A', 'AAAA')
    :type record_type: str
    :param record: The Dreamhost DNS Record's name
    :type record: str
    :param zone: The Dreamhost DNS Record's zone (the domain)
    :type zone: str
    :param comment: The Dreamhost DNS Record's comment
    :type comment: str
    :param editable: Whether or not the DNS Record is editable
    :type editable: bool
    :param remove_url: The Dreamhost API url to remove this DNS Record
    :type remove_url: str
    :param add_url: The Dreamhost API url to add this DNS Record (Dreamhost doesn't have an edit API call so you must remove and add every time)
    :type add_url: str
    :param valid_for_public_update: Whether or not this DNS Record can be updated to the public IP, true if record is editable and type is 'A'
    :type valid_for_public_update: bool
    '''

    def __init__(self, account_id, value, record_type, record, zone, comment, editable):
        '''
        Constructer method
        '''
        self.account_id = account_id
        self.value = value
        self.record_type = record_type
        self.record = record
        self.zone = zone
        self.comment = comment
        self.editable = editable == '1'
        self.remove_url = (
            f'https://api.dreamhost.com/?key={API_TOKEN}&'
            f'cmd=dns-remove_record&record={record}&type={record_type}&value={value}'
        )
        self.add_url = (
            f'https://api.dreamhost.com/?key={API_TOKEN}&'
            f'cmd=dns-add_record&record={record}&type={record_type}'
        )
        self.valid_for_public_update = self.editable and record_type == 'A'

    def __repr__(self):
        '''
        Print method
        '''
        return (
            f'<DNSRecord(account_id={self.account_id}, '
            f'value="{self.value}"", '
            f'record_type="{self.record_type}", '
            f'record="{self.record}", '
            f'zone="{self.zone}", '
            f'value="{self.value}", '
            f'remove_url="{self.remove_url}", '
            f'valid_for_public_update={self.valid_for_public_update}, '
            f'editable={self.editable}>)'
        )

    def remove_record(self):
        '''
        Deletes this DNS record using https://api.dreamhost.com/?&cmd=dns-remove_record
        '''
        get(self.remove_url)

    def update_record(self, value):
        '''
        Updates this DNS record's value using https://api.dreamhost.com/?&cmd=dns-remove_record

        :param value: The new value this record will be updated to
        :type value: str
        '''
        self.remove_record()
        add_url = self.add_url + f'&value={value}'
        get(add_url)


def list_all_records() -> List[DNSRecord]:
    '''
        Pulls all DNS records for your API token using https://api.dreamhost.com/?&cmd=dns-list_records

        :returns: A list of :class:`DNSRecord` objects
        :rtype: list[DNSRecord]
    '''
    list_url = f'https://api.dreamhost.com/?key={API_TOKEN}&cmd=dns-list_records&format=json'
    records = get(list_url).json()['data']

    l_records = []

    for record in records:
        this_record = DNSRecord(
            record['account_id'],
            record['value'],
            record['type'],
            record['record'],
            record['zone'],
            record['value'],
            record['editable'],
        )
        l_records.append(this_record)

    return l_records


def update_record_to_public_ip():
    '''
        Updates the DNS Record for the domain in settings.ini to your current public IP address.

        - Pulls your current public IP address from https://api.ipify.org
        - Pulls a list of your Dreamhost DNS records with list_all_records()
        - Finds the DNS Record that is valid_for_public_update and in the domain from settings.ini
        - If that DNS record's value is different that your current public IP, it updates it
    '''

    public_ip = get('https://api.ipify.org').content.decode('utf8')

    for record in list_all_records():
        if record.record == DOMAIN and record.valid_for_public_update:
            if record.value == public_ip:
                print('Already equal to public ip.')
            else:
                record.update_record(public_ip)
                print('Updated to public ip.')

