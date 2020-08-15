import time
import requests

from godaddypy import Client, Account

key    = "{KEY}"
secret = "{SECRET_KEY}"
domain = "{DOMAIN}"

def update():

	public_ip = requests.get('http://ip.42.pl/raw').text

	account = Account(api_key=key, api_secret=secret)
	client  = Client(account)

	record = client.get_records(domain, record_type="A")
	if record[0]['data'] != public_ip:
		print("Updating IP from {} to {}".format(record[0]['data'], public_ip))
		res = client.update_ip(public_ip, domains=[domain])

	time.sleep(300)


if __name__ == "__main__":
	
	run = True
	print("Running GoDaddy DNS Updater...")
	while run:

		try:
			update()
		except KeyboardInterrupt:
			q = input("Quit? (y/n): ")
			if q == 'y':
				run = False