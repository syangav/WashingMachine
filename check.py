import urllib, json, datetime, time, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders



def send_email(machine_number,hall,machine_type, updated_time, message):
	fromaddr = "laundry.ust.one@gmail.com"
	toaddr = "debug.ust.one@gmail.com"

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "[ERROR] %s - %s %s" %(machine_number,hall,machine_type)	 
	body = message + "something wrong! last update: " + updated_time.strftime('%Y-%m-%d %H:%M:%S')
	msg.attach(MIMEText(body, 'plain'))

	tries = 0
	while True:
	    if (tries > 60):
	        exit()
	    try:
	        server = smtplib.SMTP('smtp.gmail.com', 587)
	        break
	    except Exception as e:
	        tries = tries + 1
	        time.sleep(1)
	 
	
	server.starttls()
	server.login(fromaddr, "I_am_a_laundry")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	print('Send Report Email Successfully')
	server.quit()


allow_diff_second = 1200

down_list = []

maintenance_error_list = []

while True:

	for i in range(1, 9) :
		if ( i == 7):
			continue
		now = datetime.datetime.now()
		url = "https://ust.one/api/laundry/device-status-check/" + str(i)
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		print now

		for washer in data['washers']['data']:
			updated_time = datetime.datetime.strptime(washer["updated_at"], '%Y/%m/%d %H:%M:%S')
			# print datetime.datetime.now()
			diff_seconds =  (now - updated_time).total_seconds()
			print washer['name'] +" "+ str(diff_seconds)
			if (diff_seconds>allow_diff_second):
				if (washer["id"] not in down_list):
					# print washer["id"] + "is down"
					down_list.append(washer["id"])
					# notify
					send_email('ID:'+str(washer["id"]) +' - '+'#'+washer['name'], washer['hall'], washer['type'], updated_time, "device_power_error")
			elif washer["id"] in down_list:
				# print washer["id"] + "recovers"
				down_list.remove(washer["id"])
			if (washer['is_down'] == True and washer['remaining_minutes'] != 0 ):
				if (washer["id"] not in maintenance_error_list):
					# print washer["id"] + "'s mode needs to be updated"
					maintenance_error_list.append(washer["id"])
					# notify
					send_email('ID:'+str(washer["id"]) +' - '+'#'+washer['name'], washer['hall'], washer['type'], updated_time, "maintenance_error")
			elif washer["id"] in maintenance_error_list:
				# print washer["id"] + "mode may be ok now"
				maintenance_error_list.remove(washer["id"])


		for dryer in data['dryers']['data']:
			updated_time = datetime.datetime.strptime(dryer["updated_at"], '%Y/%m/%d %H:%M:%S')
			# print datetime.datetime.now()
			diff_seconds =  (now - updated_time).total_seconds()
			print dryer['name'] +" "+ str(diff_seconds)
			if (diff_seconds>allow_diff_second):
				if (dryer["id"] not in down_list):
					down_list.append(dryer["id"])
					# notify
					send_email('ID:'+str(dryer["id"]) +' - '+'#'+dryer['name'], dryer['hall'], dryer['type'], updated_time,  "device_power_error")
			elif dryer["id"] in down_list:
				down_list.remove(dryer["id"])	
			if (dryer['is_down'] == True and dryer['remaining_minutes'] != 0 ):
				if (dryer["id"] not in maintenance_error_list):
					# print dryer["id"] + "'s mode needs to be updated"
					maintenance_error_list.append(dryer["id"])
					# notify
					send_email('ID:'+str(dryer["id"]) +' - '+'#'+dryer['name'], dryer['hall'], dryer['type'], updated_time, "maintenance_error")
			elif dryer["id"] in maintenance_error_list:
				# print dryer["id"] + "mode may be ok now"
				maintenance_error_list.remove(dryer["id"])	

		print "down list: "
		print down_list
		print "maintenance error list: "
		print maintenance_error_list

	time.sleep(15)
