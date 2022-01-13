import os
import time
import yaml
import requests

from godaddypy import Client, Account

class Object:
	"""Object for namespace"""

def main():
	run = True
	config = get_config()

	print('Running GoDaddy DNS Updater...')
	while run:
		try:
			update(config)
		except KeyboardInterrupt:
			q = input('Quit? (y/n): ')
			if q == 'y':
				run = False
		except Exception as error:
			with open(os.path.join(os.path.dirname(__file__), 'update.log'), 'a') as f:
				f.write(str(error))

def get_config():
	with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as stream:
		config = yaml.safe_load(stream)

		config_obj = Object()

		for key, value in config.items():
			setattr(config_obj, key, value)

		return config_obj

def update(config):
	public_ip = requests.get('http://ip.42.pl/raw').text

	account = Account(api_key=config.key, api_secret=config.secret)
	client  = Client(account)

	record = client.get_records(config.domain, record_type='A')
	if record[0]['data'] != public_ip:
		print('Updating IP from {} to {}'.format(record[0]['data'], public_ip))
		client.update_ip(public_ip, domains=[config.domain])

	time.sleep(60)


if __name__ == "__main__":
	main()
