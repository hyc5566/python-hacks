from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ChromeController:
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        """初始化 Chrome"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')  # 最大化視窗
        self.driver = webdriver.Chrome(options=options)
    
    def focus_window(self):
        """將焦點轉移到 Chrome 視窗"""
        # 方法1：使用 window handles
        self.driver.switch_to.window(self.driver.current_window_handle)
        
    def switch_between_windows(self):
        """在多個視窗間切換"""
        # 開啟新分頁
        self.driver.execute_script("window.open('about:blank', 'tab2');")
        
        # 獲取所有視窗控制代碼
        handles = self.driver.window_handles
        
        # 在不同視窗間切換
        for handle in handles:
            self.driver.switch_to.window(handle)
            print(f"切換到視窗: {self.driver.title}")
            time.sleep(1)
    
    def demonstrate_window_control(self):
        """展示視窗控制的各種方法"""
        try:
            # 訪問第一個網站
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            # 最小化視窗
            self.driver.minimize_window()
            time.sleep(2)
            
            # 最大化視窗
            self.driver.maximize_window()
            time.sleep(2)
            
            # 設定視窗大小
            self.driver.set_window_size(800, 600)
            time.sleep(2)
            
            # 設定視窗位置
            self.driver.set_window_position(50, 50)
            time.sleep(2)
            
            # 全螢幕
            self.driver.fullscreen_window()
            time.sleep(2)
            
            # 獲取視窗大小和位置
            size = self.driver.get_window_size()
            position = self.driver.get_window_position()
            print(f"視窗大小: {size}")
            print(f"視窗位置: {position}")
            
            # 示範多視窗操作
            self.switch_between_windows()
            
        except Exception as e:
            print(f"發生錯誤: {e}")
    
    def cleanup(self):
        """清理資源"""
        if self.driver:
            self.driver.quit()

def main():
    controller = ChromeController()
    try:
        controller.setup_driver()
        controller.demonstrate_window_control()
        
    except Exception as e:
        print(f"主程序錯誤: {e}")
        
    finally:
        time.sleep(2)
        controller.cleanup()

if __name__ == "__main__":
    main()
