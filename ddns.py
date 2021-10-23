'''
Running the python script updates the DNS Record for the domain you set in settings.ini to your current public IP.
Set up an hourly cronjob (or any time, but hourly is more than good) to essentially have DDNS for Dreamhost.
'''
from funcs import update_record_to_public_ip

if __name__ == '__main__':
    update_record_to_public_ip()