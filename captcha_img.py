import cv2
import requests
import os
import json

# 全局变量，用来存储点击的坐标和次数
clicks = []
count = 0
max_clicks = 0


def download_image(url):
    try:
        # 获取图片的内容
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 从URL中提取图片文件名
        filename = url.split("/")[-1]

        # 确定保存路径
        filepath = os.path.join(os.getcwd(), filename)

        # 检查文件是否已经存在，若存在则删除旧文件
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"文件 '{filename}' 已存在，旧文件已删除。")

        # 以二进制写入方式保存图片
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(1024):  # 分块下载
                file.write(chunk)

        return filepath  # 返回保存的文件路径
    except Exception as e:
        print(f"Error: {e}")
        return None

# 鼠标点击事件的回调函数
def mouse_callback(event, x, y, flags, param):
    global count, max_clicks, clicks

    # 如果检测到左键点击事件
    if event == cv2.EVENT_LBUTTONDOWN:
        if count < max_clicks:
            count += 1
            clicks.append((x, y))
            # 在点击的位置绘制点击次数
            cv2.putText(img, str(count), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Image', img)

        # 当达到指定的点击次数时，关闭窗口
        if count >= max_clicks:
            cv2.destroyAllWindows()

# 主函数，接受图片路径和点击次数
def captcha_main(image_path, num_clicks):
    global img, max_clicks, clicks, count
    clicks = []
    count = 0
    max_clicks = num_clicks

    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image.")
        return

    # 创建一个窗口并显示图片
    cv2.namedWindow('Image')
    cv2.imshow('Image', img)

    # 设置鼠标点击回调函数
    cv2.setMouseCallback('Image', mouse_callback)

    # 等待用户关闭窗口
    cv2.waitKey(0)

    # 返回点击的坐标
    pos_list = [{'x': x, 'y': y} for x, y in clicks]
    return json.dumps(pos_list)

# if __name__ == "__main__":
#     image_path = "G:\\Users\\15819\\Desktop\\14_3.png"  # 替换为你的图片路径
#     num_clicks = 3  # 替换为你需要的点击次数
#     click_coordinates = captcha_main(image_path, num_clicks)
#     print("点击的坐标: ", click_coordinates)