import os
import shutil
import logging
import json
import subprocess
from datetime import datetime
import short_upload
import time
import schedule

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self, channel_config):
        """使用配置初始化处理器"""
        self.config = channel_config
        self.source_dir = channel_config['source_dir']
        self.save_dir = channel_config['save_dir']
        self.recycle_dir = channel_config['recycle_dir']
        self.device_id = channel_config['device_id']
        self.adb_device = channel_config['adb_device']
        
        # 确保目录存在
        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(self.recycle_dir, exist_ok=True)
        
    def clean_save_directory(self):
        """清理保存目录，将文件移动到回收站"""
        try:
            # 获取当前时间作为回收子文件夹名
            recycle_subdir = os.path.join(
                self.recycle_dir,
                datetime.now().strftime('%Y%m%d_%H%M%S')
            )
            
            # 检查save_dir是否有文件需要移动
            files = os.listdir(self.save_dir)
            if files:
                # 创建带时间戳的回收子文件夹
                os.makedirs(recycle_subdir, exist_ok=True)
                logger.info(f"创建回收子目录: {recycle_subdir}")
                
                # 移动文件，如果某个文件被占用则跳过
                for file in files:
                    try:
                        src_path = os.path.join(self.save_dir, file)
                        dst_path = os.path.join(recycle_subdir, file)
                        shutil.move(src_path, dst_path)
                        logger.info(f"移动文件到回收站: {file}")
                    except PermissionError as e:
                        # 如果文件被占用，记录日志并继续处理下一个文件
                        logger.warning(f"文件 {file} 被占用，跳过处理: {str(e)}")
                        continue
                    except Exception as e:
                        # 其他错误也记录并继续
                        logger.warning(f"移动文件 {file} 时出错，跳过处理: {str(e)}")
                        continue
                    
            return True
            
        except Exception as e:
            logger.error(f"清理保存目录失败: {str(e)}")
            return True  # 即使清理失败也返回 True，允许继续处理
            
    def get_next_video(self):
        """获取下一个要处理的视频"""
        try:
            # 获取源目录中的所有视频文件并按名称排序
            video_files = sorted([
                f for f in os.listdir(self.source_dir) 
                if f.lower().endswith(('.mp4', '.mov', '.avi'))
            ])
            
            # 打印所有待处理的视频文件
            logger.info(f"源目录中的视频文件列表:")
            for i, file in enumerate(video_files, 1):
                logger.info(f"{i}. {file}")
            
            if not video_files:
                logger.info("源目录中没有更多视频")
                return None
            
            # 获取第一个视频
            next_video = video_files[0]
            src_path = os.path.join(self.source_dir, next_video)
            dst_path = os.path.join(self.save_dir, next_video)
            
            # 检查源文件是否存在且可访问
            if not os.path.exists(src_path):
                logger.error(f"源文件不存在: {src_path}")
                return None
            
            try:
                # 检查文件是否可以访问
                with open(src_path, 'rb') as f:
                    pass
            except Exception as e:
                logger.error(f"无法访问源文件 {src_path}: {str(e)}")
                return None
            
            # 检查目标目录是否可写
            if not os.access(os.path.dirname(dst_path), os.W_OK):
                logger.error(f"目标目录无写入权限: {os.path.dirname(dst_path)}")
                return None
            
            # 移动（剪切）视频到保存目录
            try:
                shutil.move(src_path, dst_path)
                logger.info(f"成功移动视频到保存目录: {next_video}")
                
                # 验证文件是否成功移动
                if os.path.exists(dst_path):
                    logger.info(f"文件移动验证成功: {dst_path}")
                else:
                    logger.error(f"文件移动后未找到: {dst_path}")
                    return None
                
                return next_video
                
            except Exception as e:
                logger.error(f"移动文件时出错 {src_path} -> {dst_path}: {str(e)}")
                return None
            
        except Exception as e:
            logger.error(f"获取下一个视频失败: {str(e)}")
            # 打印更详细的错误信息
            import traceback
            logger.error(f"详细错误信息:\n{traceback.format_exc()}")
            return None

    def check_adb_connection(self):
        """检查并管理 ADB 连接"""
        try:
            import subprocess
            
            logger.info("检查 ADB 连接...")
            
            # 首先检查当前设备状态
            try:
                result = subprocess.run(
                    ['adb', 'devices'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # 如果目标设备已经正常连接，直接返回成功
                if f"{self.adb_device}\tdevice" in result.stdout:
                    logger.info(f"设备 {self.adb_device} 已正常连接")
                    return True
                    
                # 检查是否有其他设备占用
                devices = [line.split('\t')[0] for line in result.stdout.splitlines() if '\tdevice' in line]
                if devices:
                    logger.warning(f"发现其他设备连接: {devices}")
            
            except Exception as e:
                logger.warning(f"检查设备状态失败: {str(e)}")
            
            # 只有在必要时才重启 ADB 服务
            logger.info("重启 ADB 服务...")
            try:
                subprocess.run(['adb', 'kill-server'], check=True)
                time.sleep(2)
                subprocess.run(['adb', 'start-server'], check=True)
                time.sleep(3)
            except Exception as e:
                logger.error(f"重启 ADB 服务失败: {str(e)}")
                return False
            
            # 等待并验证设备连接
            max_retries = 10
            retry_interval = 5  # 秒
            
            for attempt in range(max_retries):
                try:
                    result = subprocess.run(
                        ['adb', 'devices'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    if f"{self.adb_device}\tdevice" in result.stdout:
                        logger.info(f"设备 {self.adb_device} 已连接")
                        return True
                        
                    if attempt < max_retries - 1:
                        logger.warning(f"等待设备连接 (尝试 {attempt + 1}/{max_retries})...")
                        time.sleep(retry_interval)
                        
                except Exception as e:
                    logger.warning(f"检查设备连接失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_interval)
            
            # 所有重试都失败后，发送通知
            error_msg = f"设备 {self.adb_device} 在 {max_retries} 次尝试后仍无法连接"
            logger.error(error_msg)
            self.send_alert(error_msg)  # 实现告警通知
            return False
            
        except Exception as e:
            error_msg = f"ADB 连接管理失败: {str(e)}"
            logger.error(error_msg)
            self.send_alert(error_msg)
            return False

    def send_alert(self, message):
        """发送告警通知"""
        try:
            # TODO: 实现告警通知机制
            # 例如：发送邮件、企业微信通知等
            logger.warning(f"需要发送告警: {message}")
            
            # 示例：写入错误日志文件
            with open('error_log.txt', 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now()}] {message}\n")
                
        except Exception as e:
            logger.error(f"发送告警失败: {str(e)}")

    def manage_emulator(self):
        """管理模拟器启动状态"""
        try:
            import subprocess
            import psutil
            
            logger.info(f"检查模拟器 {self.device_id} (设备: {self.adb_device}) 的状态...")
            
            # 1. 先确保 ADB 服务正常
            logger.info("重置 ADB 服务...")
            subprocess.run(['adb', 'kill-server'], check=True)
            time.sleep(2)
            subprocess.run(['adb', 'start-server'], check=True)
            time.sleep(3)
            
            # 2. 检查并关闭现有模拟器
            emulator_running = False
            for proc in psutil.process_iter(['name']):
                if proc.name() in ['LDPlayer.exe', 'dnplayer.exe']:
                    emulator_running = True
                    proc.kill()
                    logger.info(f"关闭现有模拟器进程: {proc.name()}")
            
            if emulator_running:
                time.sleep(10)  # 等待进程完全关闭
            
            # 3. 启动新的模拟器实例
            shortcut_path = rf"C:\Users\Administrator\Desktop\{self.device_id}.lnk"
            logger.info(f"启动模拟器 {self.device_id}: {shortcut_path}")
            subprocess.Popen(['cmd', '/c', 'start', '', shortcut_path])
            
            # 4. 等待模拟器启动
            logger.info("等待模拟器启动...")
            time.sleep(60)  # 增加等待时间到60秒
            
            # 5. 验证 ADB 连接和设备状态
            max_retries = 10
            retry_interval = 10  # 增加重试间隔
            
            for attempt in range(max_retries):
                try:
                    # 检查设备是否在线
                    devices_result = subprocess.run(
                        ['adb', 'devices'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    if f"{self.adb_device}\tdevice" in devices_result.stdout:
                        # 验证设备是否可以响应命令
                        version_result = subprocess.run(
                            ['adb', '-s', self.adb_device, 'shell', 'getprop', 'ro.build.version.release'],
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        
                        if version_result.stdout.strip():
                            logger.info(f"模拟器已完全就绪，Android 版本: {version_result.stdout.strip()}")
                            return True
                            
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"等待模拟器就绪... ({attempt + 1}/{max_retries}): {str(e)}")
                        time.sleep(retry_interval)
                        continue
                    else:
                        logger.error("模拟器启动验证失败")
                        return False
                        
                time.sleep(retry_interval)
                
            logger.error("模拟器启动超时")
            return False
            
        except Exception as e:
            logger.error(f"模拟器管理失败: {str(e)}")
            return False

    def process_videos(self):
        """处理所有视频"""
        try:
            # 1. 获取所有待处理视频的数量
            video_files = [f for f in os.listdir(self.source_dir) 
                          if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            total_videos = len(video_files)
            logger.info(f"总共发现 {total_videos} 个视频需要处理")
            
            videos_processed = 0
            while True:
                try:
                    # 2. 清理保存目录
                    if not self.clean_save_directory():
                        logger.error("清理保存目录失败")
                        time.sleep(60)  # 等待一分钟后继续
                        continue
                        
                    # 3. 获取并移动下一个视频
                    next_video = self.get_next_video()
                    if not next_video:
                        logger.info("没有更多视频需要处理，程序结束")
                        break
                    
                    # 4. 重启模拟器（添加重试机制）
                    emulator_retry = 3  # 最大重试次数
                    emulator_started = False
                    
                    for attempt in range(emulator_retry):
                        logger.info(f"尝试启动模拟器 (尝试 {attempt + 1}/{emulator_retry})...")
                        if self.manage_emulator():
                            emulator_started = True
                            break
                        else:
                            if attempt < emulator_retry - 1:
                                logger.warning("模拟器启动失败，等待30秒后重试...")
                                time.sleep(30)
                    
                    if not emulator_started:
                        logger.error("模拟器启动失败，等待5分钟后继续...")
                        time.sleep(300)  # 等待5分钟后继续下一轮尝试
                        continue
                    
                    # 5. 确保模拟器完全就绪
                    logger.info("等待模拟器和 ADB 完全就绪...")
                    time.sleep(10)
                    
                    # 6. 执行上传
                    logger.info(f"开始处理第 {videos_processed + 1}/{total_videos} 个视频: {next_video}")
                    device_config = {
                        'device_id': self.device_id,
                        'save_dir': self.save_dir,
                        'adb_device': self.adb_device
                    }
                    
                    upload_result = short_upload.main(device_config)
                    if upload_result:
                        videos_processed += 1
                        logger.info(f"成功处理 {videos_processed}/{total_videos} 个视频")
                    else:
                        logger.error(f"视频 {next_video} 上传失败")
                    
                    # 7. 等待1分钟后继续下一个视频
                    logger.info("等待1分钟后继续处理下一个视频...")
                    time.sleep(60)
                    
                except Exception as e:
                    logger.error(f"处理视频时出错: {str(e)}")
                    time.sleep(60)  # 出错后等待1分钟再继续
                    continue
                
            logger.info(f"所有视频处理完成，共处理 {videos_processed}/{total_videos} 个视频")
            return True
            
        except Exception as e:
            logger.error(f"视频处理过程出错: {str(e)}")
            return False

    def run_scheduled_task(self):
        """执行定时任务"""
        logger.info("开始执行定时上传任务...")
        self.process_videos()

def main():
    try:
        # 加载配置文件
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 为每个频道创建处理器并设置定时任务
        processors = {}
        for channel_id, channel_config in config['channels'].items():
            processor = VideoProcessor(channel_config)
            processors[channel_id] = processor
            
            schedule.every().day.at(channel_config['schedule_time']).do(
                processor.run_scheduled_task
            )
            logger.info(f"频道 {channel_config['name']}: 每天 {channel_config['schedule_time']} 执行")
        
        # 持续运行并检查定时任务
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)
            except KeyboardInterrupt:
                logger.info("程序被用户中断")
                break
            except Exception as e:
                logger.error(f"定时任务执行出错: {str(e)}")
                time.sleep(300)
                
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")

if __name__ == "__main__":
    logger.info("视频处理器启动...")
    logger.info("等待定时任务执行...")
    main() 