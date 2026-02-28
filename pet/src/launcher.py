# 桌宠启动器 - 带错误日志

import sys
import os
import traceback

# 设置错误日志
log_file = os.path.join(os.path.dirname(__file__), 'pet_error.log')

def log_error(msg):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")

try:
    log_error("=" * 50)
    log_error("Starting pet...")
    
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    
    log_error("PyQt6 imported successfully")
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    log_error("QApplication created")
    
    # 导入主窗口
    from main import DesktopPet
    
    log_error("DesktopPet imported")
    
    # 创建桌宠
    pet = DesktopPet()
    log_error("DesktopPet created")
    
    pet.show()
    log_error("DesktopPet shown")
    
    sys.exit(app.exec())
    
except Exception as e:
    error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
    log_error(error_msg)
    print(error_msg)
    input("Press Enter to exit...")
