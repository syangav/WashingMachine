import smtplib
import json
import socket
import requests
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

with open('/home/ustone/conf.json', 'r') as json_file:
	json_data=json_file.read().replace('\n', '')
conf = json.loads(json_data)


machine_id=conf['id']
hall = conf['hall']
machine_type = conf['type']
machine_number = conf['number']
fromaddr = "laundry.ust.one@gmail.com"
toaddr = "debug.ust.one@gmail.com"



# get ip function
def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com.hk', 0))
	print (s.getsockname()[0])
	return s.getsockname()[0]


def log(subject,image_path,cropped_path,output_path,ssocr_output,error_msg):
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "[%s] %s - %s %s" %(subject,machine_number,hall,machine_type)	 
	body = "My IP %s \nSSOCR output: %s \n" %(get_ip(),ssocr_output) 
	if(subject=='ERROR'):
		error_part = "Error Message: %s \n" %(error_msg)
		body = body+error_part
	msg.attach(MIMEText(body, 'plain'))
	 
 
	# attach in original image
	part1 = MIMEBase('application', 'octet-stream')
	part1.set_payload(open(image_path, "rb").read())
	encoders.encode_base64(part1)
	part1.add_header('Content-Disposition','attachment',filename='original_image.jpg')
	msg.attach(part1)

	# attach in original image
	part2 = MIMEBase('application', 'octet-stream')
	part2.set_payload(open(cropped_path, "rb").read())
	encoders.encode_base64(part2)
	part2.add_header('Content-Disposition','attachment',filename='cropped.jpg')
	msg.attach(part2)

	# attach in output image
	part3 = MIMEBase('application', 'octet-stream')
	part3.set_payload(open(output_path, "rb").read())
	encoders.encode_base64(part3)
	part3.add_header('Content-Disposition','attachment',filename='output.png')
	msg.attach(part3)
	 

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

def web_images(image_path,cropped_path,output_path,ssocr_output):
	url = 'https://ust.one/api/machine-images'
	files = {}
	files['original_image']=open(image_path, 'rb')
	files['cropped_image']=open(cropped_path, 'rb')
	files['output_image']=open(output_path, 'rb')
	values = {'machine_id': machine_id,'ssocr_output':ssocr_output}
	r = requests.post(url, files=files, data=values)
	return r
