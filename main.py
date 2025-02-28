import logging
import video_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("开始执行自动化流程...")
        # 直接启动视频管理器
        video_manager.main()
        
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()
