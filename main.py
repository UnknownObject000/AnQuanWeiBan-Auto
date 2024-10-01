import time
import json

import weibanapi

x_token = '57ba12f6-8ef6-4d62-8103-cb97a1bd4bbe'
user_id = 'eec6b514-93d6-4516-9e6a-e45cc3ce980c'
user_project_id = '5fc7738e-f98c-4890-8ce8-d3b06d2649da'
tenant_code = '4137011066'
#jq_id = '3410029753790258616464'



# 1.  showProgess 获取课程进度
# 2.  listCategory 获取课程分类 传入userprojectid
# 3.  listCourse 获取课程 传入categorycode
# 4.  study 传入courseid(上一步获取的resourceid)
# 5.  getCourseUrl 获取methodToken
# 6.  checkFinish(验证码用的，直接跳过)
# 7.  getNear(获取最近学习，没啥用，直接跳过)
# 8.  调用methodToken完成学习 参数callback(341+16位随机数+时间戳) _(时间戳)

def wait(text: str, ti: int):
    while ti:
        print(text % ti, end='')
        time.sleep(1)
        print('\r', end='')
        ti = ti - 1
    print('                                                                   \r', end='')


def main():
    try:
        w = weibanapi.WeibanAPI(x_token, user_id, user_project_id, tenant_code)

    except Exception:
        print('请检查初始化参数是否正确!')
        exit(-1)

    courseInfo = []

    required, finished = w.showProgress()
    print('共{}， 已完成{}'.format(required, finished))

    # 获取课程分类
    categorys = w.listCategory()
    for c in categorys:
        print("{}[{}/{}]".format(c["categoryName"], c["finishedNum"], c["totalNum"]))
        # 如果该类课程学习数 < 总数 加入到courseInfo列表中
        if c["totalNum"] > c["finishedNum"]:
            courses = w.listCourse(c["categoryCode"])
            for course in courses:
                if course["finished"] == 2:  # 根据观察 1是学了 2是没学
                    courseInfo.append(course)

    for c in courseInfo:
        userCourseId = c["userCourseId"]
        resourceName = c["resourceName"]
        categoryName = c["categoryName"]
        resourceId = c["resourceId"]
        print('开始学习{}-{}'.format(categoryName, resourceName))
        code = w.study(resourceId)
        if code != '0':
            print('开始学习失败')
            exit(-1)
        # 学太快好像有可能学不上
        wait('等待中.......%02d', 15)
        retry_cnt = 0
        captcha_id = w.DoCaptcha(userCourseId)
        while (captcha_id is None) and (retry_cnt < 5):
            retry_cnt = retry_cnt + 1
            print(f'验证码未通过，正在重试第 {retry_cnt} 次')
            captcha_id = w.DoCaptcha(userCourseId)
        if (retry_cnt >= 5):
            print('验证码重试次数达到上限，系统自动退出')
            exit(-1)
        tmp = w.MakeCourseFinish(captcha_id, userCourseId)
        res = tmp[tmp.find('({') + 1:len(tmp) - 1]
        print(f'tmp = [{tmp}], res = [{res}]')
        j = json.loads(res)
        if j["msg"] != "ok":
            print('调用MakeCourseFinish失败!')
            exit(-1)
        wait('通过! %02d s后继续', 3)


if __name__ == '__main__':
    print('免责声明： \n此程序仅供学习使用，由于个人操作引发的一系列后果与作者无关')
    main()