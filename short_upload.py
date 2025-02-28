import os
import time
import logging
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 使用相同的 desired_caps 配置
desired_caps = {
    'platformName': 'Android',
    'deviceName': 'emulator-5554',
    'platformVersion': '9',
    'appPackage': 'com.google.android.youtube',
    'appActivity': '.app.honeycomb.Shell$HomeActivity',
    'automationName': 'UiAutomator2',
    'noReset': True,
    'newCommandTimeout': 3600,
    'autoGrantPermissions': True,
    'adbExecTimeout': 60000,
    'androidDeviceReadyTimeout': 60,
    'skipServerInstallation': False,
    'skipDeviceInitialization': False,
    'noSign': True,
    'uiautomator2ServerInstallTimeout': 120000,
    'androidInstallTimeout': 120000,
    'systemPort': 8200,
    'enforceAppInstall': True,
    'autoLaunch': True,
    'autoWebview': False,
    'dontStopAppOnReset': True,
    'fullReset': False,
}

# 创建设备配置字典
DEVICE_CONFIGS = {
    'channel1': {
        'platformName': 'Android',
        'deviceName': 'emulator-5554',  # 使用 emulator 设备名
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8200,
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    },
    'channel2': {
        'platformName': 'Android',
        'deviceName': 'emulator-5556',  # 使用 emulator 设备名
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8201,  # 不同的端口
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    },
    'channel3': {  # 添加新频道的配置
        'platformName': 'Android',
        'deviceName': 'emulator-5558',  # 新设备的 ADB 名称
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8202,  # 新的端口号
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    },
    'channel4': {  # 添加新频道的配置
        'platformName': 'Android',
        'deviceName': 'emulator-5560',  # 新设备的 ADB 名称
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8203,  # 新的端口号
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    },
    'channel5': {  # 添加新频道的配置
        'platformName': 'Android',
        'deviceName': 'emulator-5562',  # 新设备的 ADB 名称
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8204,  # 新的端口号
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    },
    'channel6': {  # 添加新频道的配置
        'platformName': 'Android',
        'deviceName': 'emulator-5564',  # 新设备的 ADB 名称
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8205,  # 新的端口号
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    },
    'channel7': {  # 添加新频道的配置
        'platformName': 'Android',
        'deviceName': 'emulator-5566',  # 新设备的 ADB 名称
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8206,  # 新的端口号
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    },
    'channel8': {  # 添加新频道的配置
        'platformName': 'Android',
        'deviceName': 'emulator-5568',  # 新设备的 ADB 名称
        'platformVersion': '9',
        'appPackage': 'com.google.android.youtube',
        'appActivity': '.app.honeycomb.Shell$HomeActivity',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3600,
        'autoGrantPermissions': True,
        'adbExecTimeout': 60000,
        'androidDeviceReadyTimeout': 60,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'noSign': True,
        'uiautomator2ServerInstallTimeout': 120000,
        'androidInstallTimeout': 120000,
        'systemPort': 8207,  # 新的端口号
        'enforceAppInstall': True,
        'autoLaunch': True,
        'autoWebview': False,
        'dontStopAppOnReset': True,
        'fullReset': False,
    }
}

def test_step(driver, wait, step_name, action_func):
    """测试单个步骤"""
    logger.info(f"\n=== 测试步骤: {step_name} ===")
    try:
        result = action_func(driver, wait)
        logger.info(f"步骤 {step_name} 执行成功")
        return True
    except Exception as e:
        logger.error(f"步骤 {step_name} 执行失败: {str(e)}")
        # 保存失败时的页面信息
        with open(f'test_failures/{step_name}_failure.xml', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        return False

def step_1_plus_button(driver, wait):
    """点击＋ボタン"""
    button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//android.widget.Button[@content-desc='作成']")
    ))
    button.click()
    time.sleep(2)

def step_2_select_video(driver, wait):
    """选择视频"""
    try:
        # 等待動画選択界面加载
        time.sleep(2)
        
        # 获取屏幕尺寸
        screen_size = driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']
        
        # 计算点击坐标
        x = int(screen_width * 0.15)  # 屏幕左侧15%的位置
        y = int(screen_height * 0.2)  # 屏幕顶部20%的位置
        
        logger.info(f"点击坐标: ({x}, {y})")
        
        # 使用 TouchAction 执行单次点击
        actions = TouchAction(driver)
        actions.press(x=x, y=y).release().perform()
        
        time.sleep(2)
        return True
        
    except Exception as e:
        logger.error(f"选择视频失败: {str(e)}")
        return False

def step_3_click_next(driver, wait):
    """点击次へ按钮"""
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 先尝试使用固定坐标点击（更快）
        try:
            logger.info("尝试使用固定坐标点击次へ按钮")
            actions = TouchAction(driver)
            actions.tap(x=426, y=879).perform()  # 使用已知的准确坐标
            time.sleep(1)
            
            # 简单验证是否点击成功（检查界面变化）
            if "shorts_trim_finish_trim_button" not in driver.page_source:
                logger.info("坐标点击成功")
                logger.info(f"点击耗时: {time.time() - start_time:.2f}秒")
                return True
            else:
                logger.info("坐标点击可能未成功，尝试精确定位")
                
        except Exception as e:
            logger.info(f"坐标点击失败: {str(e)}，尝试精确定位")
        
        # 如果坐标点击失败，使用精确定位方式
        next_button = wait.until(EC.presence_of_element_located((
            By.XPATH, 
            "//android.widget.Button[@resource-id='com.google.android.youtube:id/shorts_trim_finish_trim_button']"
        )))
        next_button.click()
        logger.info(f"精确定位点击成功，总耗时: {time.time() - start_time:.2f}秒")
        return True
        
    except Exception as e:
        logger.error(f"点击次へ按钮失败: {str(e)}")
        return False

def step_4_add_sound(driver, wait):
    """点击サウンドを追加"""
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 先尝试使用固定坐标点击（更快）
        try:
            logger.info("尝试使用固定坐标点击サウンドを追加")
            actions = TouchAction(driver)
            actions.tap(x=151, y=60).perform()  # 使用已知的准确坐标
            time.sleep(1)
            
            # 简单验证是否点击成功
            if "shorts_edit_sound_button" not in driver.page_source:
                logger.info("坐标点击成功")
                logger.info(f"点击耗时: {time.time() - start_time:.2f}秒")
                return True
            else:
                logger.info("坐标点击可能未成功，尝试其他方法")
                
        except Exception as e:
            logger.info(f"坐标点击失败: {str(e)}，尝试其他方法")
        
        # 如果坐标点击失败，尝试通过 resource-id 定位
        try:
            add_sound = wait.until(EC.presence_of_element_located(
                (By.ID, "com.google.android.youtube:id/shorts_edit_sound_button")
            ))
            add_sound.click()
            logger.info(f"通过 resource-id 点击成功，总耗时: {time.time() - start_time:.2f}秒")
            return True
        except:
            logger.info("通过 resource-id 定位失败，尝试最后方法")
            
        # 最后尝试通过 content-desc 定位
        add_sound = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//android.view.ViewGroup[@content-desc='サウンドを追加']")
        ))
        add_sound.click()
        logger.info(f"通过 content-desc 点击成功，总耗时: {time.time() - start_time:.2f}秒")
        return True
        
    except Exception as e:
        logger.error(f"点击サウンドを追加失败: {str(e)}")
        logger.info(f"总耗时: {time.time() - start_time:.2f}秒")
        return False

def step_5_saved_music(driver, wait):
    """点击保存済み"""
    time.sleep(1)
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 通过文本内容定位（最快的方法）
        logger.info("通过文本内容定位保存済み按钮")
        saved = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[@text='保存済み']")
        ))
        saved.click()
        
        logger.info(f"点击成功，耗时: {time.time() - start_time:.2f}秒")
        return True
        
    except Exception as e:
        logger.error(f"点击保存済み失败: {str(e)}")
        logger.info(f"总耗时: {time.time() - start_time:.2f}秒")
        return False

def step_6_select_first_song(driver, wait):
    """选择第一首曲子"""
    try:
        max_attempts = 3  # 最大尝试次数
        start_time = time.time()
        time.sleep(2)  # 等待界面稳定
        
        for attempt in range(max_attempts):
            logger.info(f"第 {attempt + 1} 次尝试")
            
            # 选择第一首歌
            first_song = wait.until(EC.presence_of_element_located(
                (By.XPATH, "(//android.view.ViewGroup[@clickable='true'])[1]")
            ))
            
            # 获取歌曲元素的位置和大小
            song_location = first_song.location
            song_size = first_song.size
            logger.info(f"歌曲位置: {song_location}, 大小: {song_size}")
            
            # 点击歌曲
            first_song.click()
            logger.info("已点击第一首歌，等待状态变化")
            
            # 等待3秒检查状态是否变化
            arrow_appeared = False
            wait_start = time.time()
            
            # 先等待1秒让界面稳定
            time.sleep(1)
            
            # 然后开始检查状态变化
            while time.time() - wait_start < 3:  # 增加到3秒
                try:
                    # 检查歌曲状态是否变为"プレビューを停止"
                    if "プレビューを停止" in driver.page_source:
                        arrow_appeared = True
                        logger.info(f"状态已改变，用时: {time.time() - wait_start:.3f}秒")
                        # 再等待2秒确保箭头稳定显示
                        time.sleep(2)
                        break
                    time.sleep(0.1)
                except:
                    pass
            
            if not arrow_appeared:
                logger.info("3秒内未检测到状态变化，将重试")
                continue
            
            # 计算箭头的位置（在歌曲最右侧）
            arrow_x = song_location['x'] + song_size['width'] + 50  # 歌曲最右侧偏移50像素
            arrow_y = song_location['y'] + (song_size['height'] / 2)  # 垂直居中
            
            logger.info(f"点击箭头位置: ({arrow_x}, {arrow_y})")
            actions = TouchAction(driver)
            actions.tap(x=int(arrow_x), y=int(arrow_y)).perform()
            
            # 等待一小段时间确认点击成功
            time.sleep(1)
            
            logger.info(f"步骤完成，总耗时: {time.time() - start_time:.2f}秒")
            return True
            
        logger.error("达到最大尝试次数，选择歌曲失败")
        return False
        
    except Exception as e:
        logger.error(f"选择第一首曲子失败: {str(e)}")
        return False

def step_8_volume_button(driver, wait):
    """点击音量调整按钮"""
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 方法1：通过 resource-id 定位（最准确的方法）
        try:
            method_start = time.time()
            logger.info("尝试方法1: 通过 resource-id 定位")
            volume = wait.until(EC.presence_of_element_located(
                (By.ID, "com.google.android.youtube:id/shorts_edit_volume_button")
            ))
            volume.click()
            logger.info(f"方法1成功，耗时: {time.time() - method_start:.2f}秒")
            time.sleep(1)  # 等待界面响应
            return True
            
        except Exception as e:
            logger.info(f"方法1失败: {str(e)}")
        
        # 方法2：通过 content-desc 定位
        try:
            method_start = time.time()
            logger.info("尝试方法2: 通过 content-desc 定位")
            volume = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//android.widget.FrameLayout[@content-desc='音量']")
            ))
            volume.click()
            logger.info(f"方法2成功，耗时: {time.time() - method_start:.2f}秒")
            time.sleep(1)  # 等待界面响应
            return True
            
        except Exception as e:
            logger.info(f"方法2失败: {str(e)}")
        
        # 方法3：使用准确坐标点击
        try:
            method_start = time.time()
            logger.info("尝试方法3: 使用准确坐标点击")
            # 使用元素信息中的准确坐标
            x = 444 + (96 // 2)  # x坐标 + 宽度的一半
            y = 45 + (87 // 2)   # y坐标 + 高度的一半
            
            logger.info(f"点击坐标: ({x}, {y})")
            actions = TouchAction(driver)
            actions.tap(x=x, y=y).perform()
            
            logger.info(f"方法3成功，耗时: {time.time() - method_start:.2f}秒")
            time.sleep(1)  # 等待界面响应
            return True
            
        except Exception as e:
            logger.info(f"方法3失败: {str(e)}")
        
        logger.error("所有方法都失败了")
        logger.info(f"总耗时: {time.time() - start_time:.2f}秒")
        return False
        
    except Exception as e:
        logger.error(f"点击音量调整按钮失败: {str(e)}")
        return False

def step_9_adjust_added_sound(driver, wait):
    """调整追加音声音量到100%"""
    try:
        # 等待滑块加载
        slider = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//android.widget.SeekBar[1]")
        ))
        
        # 获取滑块的位置和大小
        size = slider.size
        location = slider.location
        
        # 直接点击目标位置（100%
        target_x = location['x'] + (size['width'] * 0.95)  # 95%位置
        target_y = location['y'] + (size['height'] / 2)    # 垂直中间
        
        logger.info(f"点击追加音声音量位置: ({target_x}, {target_y})")
        
        # 使用点击而不是滑动
        actions = TouchAction(driver)
        actions.tap(x=int(target_x), y=int(target_y)).perform()
        
        time.sleep(1)
        return True
        
    except Exception as e:
        logger.error(f"调整追加音声音失败: {str(e)}")
        return False

def step_10_adjust_bgm(driver, wait):
    """调整BGM音量到30%"""
    try:
        # 等待第一个滑块加载（追加音声）
        first_slider = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//android.widget.SeekBar[1]")
        ))
        
        # 获取第一个滑块的位置
        first_location = first_slider.location
        first_size = first_slider.size
        
        # BGM 滑块在第一个滑块下100像素
        target_x = first_location['x'] + (first_size['width'] * 0.3)  # 30%位置
        target_y = first_location['y'] + first_size['height'] + 100   # 下方100像素
        
        logger.info(f"点击BGM音量位置: ({target_x}, {target_y})")
        
        # 使用点击而不是滑动
        actions = TouchAction(driver)
        actions.tap(x=int(target_x), y=int(target_y)).perform()
        
        time.sleep(1)
        return True
        
    except Exception as e:
        logger.error(f"调整BGM音量失败: {str(e)}")
        return False

def check_bgm_volume(driver):
    """检查BGM音量是否调整成功"""
    try:
        slider = driver.find_element(By.XPATH, "//android.widget.SeekBar[2]")
        value = slider.get_attribute('value')
        logger.info(f"当前BGM音值: {value}")
        return True
    except:
        return False

def step_11_confirm_volume(driver, wait):
    """点击完了按钮"""
    try:
        # 记录开始时间
        start_time = time.time()
        time.sleep(1)  # 等待界面稳定
        
        # 方法1：通过 resource-id 定位（最准确的方法）
        try:
            method_start = time.time()
            logger.info("尝试方法1: 通过 resource-id 定位")
            confirm = wait.until(EC.presence_of_element_located(
                (By.ID, "com.google.android.youtube:id/button_done")
            ))
            confirm.click()
            logger.info(f"方法1成功，耗时: {time.time() - method_start:.2f}秒")
            return True
            
        except Exception as e:
            logger.info(f"方法1失败: {str(e)}")
        
        # 方法2：通过 content-desc 定位
        try:
            method_start = time.time()
            logger.info("尝试方法2: 通过 content-desc 定位")
            confirm = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//android.widget.ImageView[@content-desc='完了']")
            ))
            confirm.click()
            logger.info(f"方法2成功，耗时: {time.time() - method_start:.2f}秒")
            return True
            
        except Exception as e:
            logger.info(f"方法2失败: {str(e)}")
        
        # 方法3：使用准确坐标点击
        try:
            method_start = time.time()
            logger.info("尝试方法3: 使用准确坐标点击")
            # 使用元素信息中的准确坐标
            x = 468 + (72 // 2)  # x坐标 + 宽度的一半
            y = 600 + (72 // 2)  # y坐标 + 高度的一半
            
            logger.info(f"点击坐标: ({x}, {y})")
            actions = TouchAction(driver)
            actions.tap(x=x, y=y).perform()
            
            logger.info(f"方法3成功，耗时: {time.time() - method_start:.2f}秒")
            return True
            
        except Exception as e:
            logger.info(f"方法3失败: {str(e)}")
        
        logger.error("所有方法都失败了")
        logger.info(f"总耗时: {time.time() - start_time:.2f}秒")
        return False
        
    except Exception as e:
        logger.error(f"点击完了按钮失败: {str(e)}")
        return False

def step_12_click_next_for_title(driver, wait):
    """点击次へ进入标题界面"""
    try:
        # 记录开始时间
        start_time = time.time()
        time.sleep(1)  # 等待界面稳定
        
        # 方法1：通过 resource-id 定位（最准确的方法）
        try:
            method_start = time.time()
            logger.info("尝试方法1: 通过 resource-id 定位")
            next_button = wait.until(EC.presence_of_element_located(
                (By.ID, "com.google.android.youtube:id/shorts_post_bottom_button")
            ))
            next_button.click()
            logger.info(f"方法1成功，耗时: {time.time() - method_start:.3f}秒")
            time.sleep(1)  # 等待界面响应
            return True
            
        except Exception as e:
            logger.info(f"方法1失败: {str(e)}")
        
        # 方法2：通过文本内容定位
        try:
            method_start = time.time()
            logger.info("尝试方法2: 通过文本内容定位")
            next_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//android.widget.Button[@text='次へ']")
            ))
            next_button.click()
            logger.info(f"方法2成功，耗时: {time.time() - method_start:.3f}秒")
            time.sleep(1)  # 等待界面响应
            return True
            
        except Exception as e:
            logger.info(f"方法2失败: {str(e)}")
        
        # 方法3：使用准确坐标点击
        try:
            method_start = time.time()
            logger.info("尝试方法3: 使用准确坐标点击")
            # 使用元素信息中的准确坐标
            x = 279 + (237 // 2)  # x坐标 + 宽度的一半
            y = 885 + (60 // 2)   # y坐标 + 高度的一半
            
            logger.info(f"点击坐标: ({x}, {y})")
            actions = TouchAction(driver)
            actions.tap(x=x, y=y).perform()
            
            logger.info(f"方法3成功，耗时: {time.time() - method_start:.3f}秒")
            time.sleep(1)  # 等待界面响应
            return True
            
        except Exception as e:
            logger.info(f"方法3失败: {str(e)}")
        
        logger.error("所有方法都失败了")
        logger.info(f"总耗时: {time.time() - start_time:.2f}秒")
        return False
        
    except Exception as e:
        logger.error(f"点击次へ按钮失败: {str(e)}")
        return False

def get_video_filename(directory):
    """获取指定目录中的第一个视频文件名"""
    try:
        # 获取目录中的所有文件
        files = os.listdir(directory)
        # 过滤出视频文件（可以根据需要添加其他视频格式）
        video_files = [f for f in files if f.lower().endswith(('.mp4', '.mov', '.avi'))]
        if video_files:
            return os.path.join(directory, video_files[0])
        else:
            raise Exception(f"在目录 {directory} 中未找到视频文件")
    except Exception as e:
        logger.error(f"获取视频文件名失败: {str(e)}")
        raise

def step_13_input_title(driver, wait, video_directory):
    """输入标题"""
    try:
        # 记录开始时间
        start_time = time.time()
        time.sleep(1)  # 等待界面稳定
        
        # 获取视频文件路径并提取文件名
        try:
            method_start = time.time()
            logger.info("获取视频文件名...")
            video_path = get_video_filename(video_directory)
            title = os.path.splitext(os.path.basename(video_path))[0]
            logger.info(f"视频标题: {title}, 耗时: {time.time() - method_start:.3f}秒")
        except Exception as e:
            logger.error(f"获取视频文件名失败: {str(e)}")
            return False
        
        # 方法1：通过准确坐标定位（最快）
        try:
            method_start = time.time()
            logger.info("尝试方法1: 通过准确坐标定位")
            
            # 使用元素信息中的准确坐标
            x = 164 + (522 - 164) // 2  # 输入框中心x坐标
            y = 298 + (354 - 298) // 2  # 输入框中心y坐标
            
            actions = TouchAction(driver)
            actions.tap(x=x, y=y).perform()
            time.sleep(0.5)  # 等待输入框获得焦点
            
            # 清除现有文本
            driver.press_keycode(123)  # KEYCODE_MOVE_END
            for _ in range(50):  # 足够多的删除操作
                driver.press_keycode(67)  # KEYCODE_DEL
            
            # 输入新标题
            driver.set_value(driver.switch_to.active_element, title)
            
            logger.info(f"方法1成功，耗时: {time.time() - method_start:.3f}秒")
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.info(f"方法1失败: {str(e)}")
        
        # 方法2：通过class和text组合定位
        try:
            method_start = time.time()
            logger.info("尝试方法2: 通过class和text定位")
            title_input = wait.until(EC.presence_of_element_located((
                By.XPATH, 
                "//android.widget.EditText[@text='ショート動画にキャプションを付ける']"
            )))
            
            title_input.clear()
            time.sleep(0.5)
            title_input.send_keys(title)
            
            logger.info(f"方法2成功，耗时: {time.time() - method_start:.3f}秒")
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.info(f"方法2失败: {str(e)}")
        
        # 方法3：通过bounds定位
        try:
            method_start = time.time()
            logger.info("尝试方法3: 通过bounds定位")
            title_input = wait.until(EC.presence_of_element_located((
                By.XPATH, 
                "//android.widget.EditText[@bounds='[164,298][522,354]']"
            )))
            
            title_input.clear()
            time.sleep(0.5)
            title_input.send_keys(title)
            
            logger.info(f"方法3成功，耗时: {time.time() - method_start:.3f}秒")
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.info(f"方法3失败: {str(e)}")
        
        # 隐藏键盘（如果显示）
        try:
            driver.hide_keyboard()
        except:
            pass
        
        logger.error("所有方法都失败了")
        logger.info(f"总耗时: {time.time() - start_time:.2f}秒")
        return False
        
    except Exception as e:
        logger.error(f"输入标题失败: {str(e)}")
        return False

def step_14_click_upload(driver, wait):
    """点击上传按钮"""
    try:
        # 记录开始时间
        start_time = time.time()
        time.sleep(1)  # 等待界面稳定
        
        # 方法1：通过 resource-id 定位（最准确的方法）
        try:
            method_start = time.time()
            logger.info("尝试方法1: 通过 resource-id 定位")
            upload_button = wait.until(EC.presence_of_element_located(
                (By.ID, "com.google.android.youtube:id/upload_bottom_button")
            ))
            upload_button.click()
            logger.info(f"方法1成功，耗时: {time.time() - method_start:.3f}秒")
            logger.info("等待上传开始...")
            time.sleep(10)  # 等待上传开始并确保上传已经启动
            return True
            
        except Exception as e:
            logger.info(f"方法1失败: {str(e)}")
        
        # 方法2：通过文本内容定位
        try:
            method_start = time.time()
            logger.info("尝试方法2: 通过文本内容定位")
            upload_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//android.widget.Button[@text='ショート動画をアップロード']")
            ))
            upload_button.click()
            logger.info(f"方法2成功，耗时: {time.time() - method_start:.3f}秒")
            logger.info("等待上传开始...")
            time.sleep(10)  # 等待上传开始并确保上传已经启动
            return True
            
        except Exception as e:
            logger.info(f"方法2失败: {str(e)}")
        
        # 方法3：使用准确坐标点击
        try:
            method_start = time.time()
            logger.info("尝试方法3: 使用准确坐标点击")
            # 使用元素信息中的准确坐标
            x = 18 + (504 // 2)  # x坐标 + 宽度的一半
            y = 837 + (72 // 2)  # y坐标 + 高度的一半
            
            logger.info(f"点击坐标: ({x}, {y})")
            actions = TouchAction(driver)
            actions.tap(x=x, y=y).perform()
            
            logger.info(f"方法3成功，耗时: {time.time() - method_start:.3f}秒")
            logger.info("等待上传开始...")
            time.sleep(10)  # 等待上传开始并确保上传已经启动
            return True
            
        except Exception as e:
            logger.info(f"方法3失败: {str(e)}")
        
        logger.error("所有方法都失败了")
        logger.info(f"总耗时: {time.time() - start_time:.2f}秒")
        return False
        
    except Exception as e:
        logger.error(f"点击上传按钮失败: {str(e)}")
        return False

def main(device_config=None):
    driver = None
    total_start_time = time.time()
    try:
        if not device_config:
            raise ValueError("未提供设备配置")
            
        # 获取设备配置
          # 修改设备配置选择逻辑
        channel = 'channel1'
        if device_config:
            if device_config.get('device_id') == '02':
                channel = 'channel2'
            elif device_config.get('device_id') == '03':
                channel = 'channel3'
            elif device_config.get('device_id') == '04':
                channel = 'channel4'
            elif device_config.get('device_id') == '05':
                channel = 'channel5'
            elif device_config.get('device_id') == '06':
                channel = 'channel6'
            elif device_config.get('device_id') == '07':
                channel = 'channel7'
            elif device_config.get('device_id') == '08':
                channel = 'channel8'


        caps = DEVICE_CONFIGS[channel]
        
        # 使用传入的 ADB 设备信息
        if 'adb_device' in device_config:
            caps['deviceName'] = device_config['adb_device']
        
        # 获取视频保存目录
        video_directory = device_config.get('save_dir', r"C:\AppiumLD\savevideo")
        
        # 初始化 Appium 会话
        logger.info(f"初始化 Appium 会话 (设备: {caps['deviceName']})")
        driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
        wait = WebDriverWait(driver, 30)
        
        # 执行上传步骤
        steps = [
            ("plus_button", step_1_plus_button),
            ("select_video", step_2_select_video),
            ("click_next", step_3_click_next),
            ("add_sound", step_4_add_sound),
            ("saved_music", step_5_saved_music),
            ("select_first_song", step_6_select_first_song),
            ("volume_button", step_8_volume_button),
            ("adjust_added_sound", step_9_adjust_added_sound),
            ("adjust_bgm", step_10_adjust_bgm),
            ("confirm_volume", step_11_confirm_volume),
            ("click_next_for_title", step_12_click_next_for_title),
            ("input_title", lambda d, w: step_13_input_title(d, w, video_directory)),
            ("click_upload", step_14_click_upload),
        ]
        
        # 记录每个步骤的耗时
        step_times = {}
        
        for step_name, step_func in steps:
            step_start = time.time()
            if not test_step(driver, wait, step_name, step_func):
                logger.error(f"测试在步骤 {step_name} 失败，终止测试")
                return False
            step_times[step_name] = time.time() - step_start
            
        # 计算总耗时
        total_time = time.time() - total_start_time
        
        # 输出详细的时间统计
        logger.info("\n=== 时间统计 ===")
        logger.info(f"总耗时: {total_time:.2f}秒")
        logger.info("\n各步骤耗时:")
        for step_name, step_time in step_times.items():
            logger.info(f"{step_name}: {step_time:.2f}秒")
        
        logger.info("\n所有步骤测试完成！")
        return True
        
    except Exception as e:
        logger.error(f"测试过程出错: {str(e)}")
        total_time = time.time() - total_start_time
        logger.info(f"执行中断，总耗时: {total_time:.2f}秒")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main() 