import requests
import numpy as np
import cv2
import easyocr
from bs4 import BeautifulSoup


def get_captcha_and_sessid():    
    while True:
      image = requests.get('http://101.251.6.66/captcha.php')
      COOKIE_CODE = image.cookies.values()[0]
      captcha = decode_captcha(image)
      HEADERS = {
      'Cookie': f'PHPSESSID={COOKIE_CODE}',
      'Content-Type': 'application/x-www-form-urlencoded'
      }
    
      dummy_payload = {
                  "mode": "resView",
                  "frmAction": "submit",
                  "regNumber": 'xx',
                  "dob": '2003-05-12',
                  "examType": 'Regular',
                  "examYear": '2022',
                  "semYear": 'I',
                  "semPart": 'II',
                  "captcha": str(captcha)
              }
      res = requests.post(
        'http://101.251.6.66/index.php'
          , headers=HEADERS
          , data=dummy_payload
      )
      captcha_text = parse_captcha_div(res)
      if 'captcha' in captcha_text.lower():
        print('Model predicted wrong CAPTCHA, trying again...')
        
      else:
        print('Correct CAPTCHA acquired')
        return COOKIE_CODE, captcha

def parse_captcha_div(res):
    soup = BeautifulSoup(res.content, 'html.parser') 
    captcha_div = soup.find('div')
    captcha_text = captcha_div.get_text()
    return captcha_text

def decode_captcha(image):
    arr = np.frombuffer(image.content, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    black_threshold = 120
    white_threshold = 190
    img = np.where((img < black_threshold) | (img > white_threshold), 10, 255)
    images = numbers_cutout(img)
    text = return_string(images)
    print('YOUR CAPTCHA IS:', text)
    return text

def return_string(images):
    n = []
    gap = np.ones((25,2))*255
    gap_tb = np.ones((2,120))*255
    for img in images:
        resized_image = cv2.resize(img, (20, 25), interpolation=cv2.INTER_NEAREST)
        n.append(gap)
        n.append(resized_image)
        n.append(gap)    
    x = np.concatenate(n, axis=1)
    x = np.concatenate((gap_tb, x, gap_tb))
    return num_reader(x)

def num_reader(img):
  reader = easyocr.Reader(['en'])

  # Path to the image containing numbers
  imgg = cv2.convertScaleAbs(img)
  # Perform OCR on the image to extract numbers
  result = reader.readtext(imgg, detail=0, allowlist='0123456789')
  return ''.join(result)

def vertical_cutouts(img_t):
  y_pos = []
  allow = 0 #0-top of a number, 1-bottom of a number

  means = np.mean(img_t, axis=1)
  top = 0
  end = len(means)-1
  for index, item in enumerate(means):
    if allow==0 and item !=255:
      top = index - 1 if index != 0 else index  
      allow = 1
    
    elif allow==1 and item == 255:
      y_pos.append((top, index+1))
      allow = 0
    elif allow==1 and index==end:
      y_pos.append((top, end))
  return y_pos

def horizontal_cutouts(img_t, y_positions):
  final_cutouts = []
  for y_pos in y_positions:
    img_y_cut_transposed = img_t[y_pos[0]:y_pos[1]]
    img = np.transpose(img_y_cut_transposed)
    pos = vertical_cutouts(img)[0]
    final_img = img[pos[0]:pos[1]]
    final_cutouts.append(final_img)
  return final_cutouts

def numbers_cutout(img):
  img_t = np.transpose(img)
  y_positions = vertical_cutouts(img_t)
  images = horizontal_cutouts(img_t, y_positions)
  return images