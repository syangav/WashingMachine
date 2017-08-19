import smtplib
import json
import get_ip
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

with open('/home/ustone/conf.json', 'r') as json_file:
	json_data=json_file.read().replace('\n', '')
identity = json.loads(json_data)

hall = identity['hall']
machine_type = identity['type']
machine_number = identity['number']
fromaddr = "laundry.ust.one@gmail.com"
toaddr = "debug.ust.one@gmail.com"


def send_email(image_path,ssocr_output):
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "[TEST IMAGE] %s - %s %s" %(machine_number,hall,machine_type)	 
	body = "My IP %s \n SSOCR output is %s \n\n\n\n\n\n\n" %(get_ip.get_ip(),ssocr_output) 
	msg.attach(MIMEText(body, 'plain'))
	 
	filename = "test_image.jpg"
	attachment = open(image_path, "rb")
	 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	 
	msg.attach(part)
	 

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
	print('Send Email Successfully')
	server.quit()