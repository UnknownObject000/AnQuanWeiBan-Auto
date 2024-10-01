import datetime
import json
import random
import requests
import time
import captcha_img


def get_timestamp():
    return str(round(datetime.datetime.now().timestamp(), 3))


def parseMethodToken(test: str):
    return test[test.find('methodToken=') + 12:test.find('&csComm')]

#https://mcwk.mycourse.cn/course/A22002/A22002.html?userCourseId57051d99-434f-4814-81e7-84deee2128bb\u0026tenantCode\u003d4137011066\u0026type\u003d1\u0026csComm\u003dtrue\u0026csCapt\u003dtrue
#https://mcwk.mycourse.cn/course/A22002/A22002.html?userCourseId=57051d99-434f-4814-81e7-84deee2128bb&tenantCode=4137011066&type=1&csComm=true&csCapt=true
#https://mcwk.mycourse.cn/course/A22002/A22002.html?userCourseId=57051d99-434f-4814-81e7-84deee2128bb&tenantCode=4137011066&type=1&csComm=true&csCapt=true&userProjectId=5fc7738e-f98c-4890-8ce8-d3b06d2649da&userId=eec6b514-93d6-4516-9e6a-e45cc3ce980c&courseId=dd85f614-d32f-11eb-9a88-d4ae52bad611&projectType=special&projectId=undefined&protocol=true&link=34415&weiban=weiban&userName=f61f3acc85f34ae5802675ac194a5c38
#https://weiban.mycourse.cn/#/course/detail?courseId=dd85f614-d32f-11eb-9a88-d4ae52bad611&userProjectId=5fc7738e-f98c-4890-8ce8-d3b06d2649da&courseName=%E5%8F%8D%E6%81%90%E4%B9%8B%E3%80%8A%E5%8F%8D%E6%81%90%E6%B3%95%E3%80%8B%E7%AF%87&userCourseId=57051d99-434f-4814-81e7-84deee2128bb&link=34415&projectType=special

def GetTimeStampMS():
    return str(int(round(time.time() * 1000)))


class WeibanAPI:
    tenantCode = ''
    x_token = ' '
    userId = ' '
    userProjectId = ' '
    headers = None
    captcha_headers = None

    def __init__(self, token, user_id, user_project_id, tenant_code):
        self.x_token = token
        self.tenantCode = tenant_code
        self.userId = user_id
        self.userProjectId = user_project_id
        self.headers = {
            'X-Token': self.x_token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'
        }
        self.captcha_headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
            'Referer': 'https://mcwk.mycourse.cn/'
        }
        res = self._showProgress()
        if len(res) == 0:
            raise Exception('failed to get course info')

    def showProgress(self):
        res = self._showProgress()
        j = json.loads(res)
        return j["data"]["requiredNum"], j["data"]["requiredFinishedNum"]

    def _showProgress(self):
        url = 'https://weiban.mycourse.cn/pharos/project/showProgress.do?timestamp=' + get_timestamp()
        data = {
            'tenantCode': self.tenantCode,
            'userId': self.userId,
            'userProjectId': self.userProjectId
        }
        return self.process_url(url, data)

    def _process_url(self, url, param, method):
        if method == 'POST':
            re = requests.post(url=url, data=param, headers=self.headers)
        elif method == 'GET':
            url += '?'
            for key, item in param.items():
                url = url + ('' if url.endswith('?') else '&') + str(key) + '=' + str(item)
            re = requests.get(url=url, headers=self.headers)
        else:
            raise ValueError('WRONG METHOD')
        return re.text

    def process_url(self, url, param, method='POST'):
        return self._process_url(url, param, method)

    def _listCategory(self):
        url = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp=' + get_timestamp()
        data = {
            'tenantCode': self.tenantCode,
            'userId': self.userId,
            'userProjectId': self.userProjectId,
            'chooseType': 3
        }
        return self.process_url(url, data)

    def listCategory(self):
        ret = self._listCategory()
        try:
            j = json.loads(ret)
            return j["data"]
        except json.decoder.JSONDecodeError as e:
            print(e.msg)

    def _listCourse(self, category_code):
        url = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp=' + get_timestamp()
        data = {
            'tenantCode': self.tenantCode,
            'userId': self.userId,
            'userProjectId': self.userProjectId,
            'chooseType': 3,
            'categoryCode': category_code
        }
        return self.process_url(url, data)

    def listCourse(self, category_code):
        ret = self._listCourse(category_code)
        try:
            j = json.loads(ret)
            return j["data"]
        except json.decoder.JSONDecodeError as e:
            print(e.msg)

    def _getCourseUrl(self, resource_id):
        url = 'https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do?timestamp=' + get_timestamp()
        data = {
            'tenantCode': self.tenantCode,
            'userId': self.userId,
            'userProjectId': self.userProjectId,
            'courseId': resource_id
        }
        return self.process_url(url, data)

    def getCourseUrl(self, resource_id):
        ret = self._getCourseUrl(resource_id)
        try:
            j = json.loads(ret)
            return j["data"]
        except json.decoder.JSONDecodeError as e:
            print(e.msg)

    def methodToken(self, method_token, user_course_id):
        url = 'https://weiban.mycourse.cn/pharos/usercourse/v1/{}.do'.format(method_token)
        t = get_timestamp().replace('.', '')
        param = {
            'callback': 'jQuery341' + str(random.random()).replace('.', '') + '_' + t,
            'userCourseId': user_course_id,
            'tenantCode': self.tenantCode,
            '_': int(t) + 1
        }
        return self.process_url(url, param, 'GET')

    def CheckCaptcha(self, url, answer):
        payload = {"coordinateXYs": answer}
        return requests.post(url, data=payload, headers=self.captcha_headers).text

    def DoCaptcha(self, user_course_id):
        get_url = 'https://weiban.mycourse.cn/pharos/usercourse/getCaptcha.do'
        check_url = 'https://weiban.mycourse.cn/pharos/usercourse/checkCaptcha.do'
        #?userCourseId={}&userProjectId={}&userId={}&tenantCode={}
        param = {
            'userCourseId': user_course_id,
            'userProjectId': self.userProjectId,
            'userId': self.userId,
            'tenantCode': self.tenantCode
        }
        try:
            captcha_data = json.loads(self.process_url(get_url, param, 'GET'))
            captcha_num = captcha_data["captcha"]["num"]
            captcha_id = captcha_data["captcha"]["questionId"]
            captcha_image = captcha_img.download_image(captcha_data["captcha"]["imageUrl"])
            if(captcha_image is None):
                print('【错误】无法下载验证码')
                return None
            answer_pos = captcha_img.captcha_main(captcha_image, captcha_num)
            full_check_url = f'{check_url}?userCourseId={user_course_id}&userProjectId={self.userProjectId}&userId={self.userId}&tenantCode={self.tenantCode}&questionId={captcha_id}'
            captcha_result = json.loads(self.CheckCaptcha(full_check_url, answer_pos))
            if((captcha_result["code"] != "0") or (captcha_result["data"]["checkResult"] != 1)):
                print('【错误】验证码未通过')
                return None
            return captcha_result["data"]["methodToken"]
        except json.decoder.JSONDecodeError as e:
            print(f'JSON Error: {e.msg}')
            return None

    def MakeCourseFinish(self, captcha_token, user_course_id):
        url = 'https://weiban.mycourse.cn/pharos/usercourse/v2/{}.do'.format(captcha_token)
        t = GetTimeStampMS()
        param = {
            'callback': 'jQuery341' + str(random.random()).replace('.', '') + '_' + t,
            'userCourseId': user_course_id,
            'tenantCode': self.tenantCode,
            '_': int(t) + 1
        }
        return self.process_url(url, param, 'GET')

    def study(self, resource_id):
        res = self._study(resource_id)
        try:
            j = json.loads(res)
            return j["code"]
        except json.decoder.JSONDecodeError as e:
            print(e.msg)

    def _study(self, resource_id):
        url = 'https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp=' + get_timestamp()
        data = {
            'tenantCode': self.tenantCode,
            'userId': self.userId,
            'userProjectId': self.userProjectId,
            'courseId': resource_id
        }
        return self.process_url(url, data)