"""
Linux操作系统适配器实现
"""

import sys
import time
import io
import getpass
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QBuffer, QIODevice
from .base_adapter import BaseOSAdapter


class LinuxAdapter(BaseOSAdapter):
    """Linux操作系统适配器"""
    
    # 在类初始化方法中添加以下代码
    def __init__(self):
        try:
            import os
            # 检测是否在 Wayland 环境下运行，如果是则设置平台变量
            if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
                os.environ['QT_QPA_PLATFORM'] = 'wayland'
                print("注意：在Wayland环境下运行，键盘监听功能可能受限")
                
            # 导入keyboard库
            import keyboard
            from PIL import Image
            
            self.keyboard = keyboard
            self.Image = Image
            
            # 存储热键ID，用于后续取消注册
            self.hotkey_id = None
            # 线程控制标志
            self.running = False
            # 监听线程
            self.listener_thread = None
            
            # 添加以下实例变量
            self.is_processing = False
            self.last_trigger_time = 0
            self.TRIGGER_INTERVAL = 0.5
            
            # 在Linux上初始化QApplication
            self.app = QApplication.instance()
            if self.app is None:
                self.app = QApplication([])
        except ImportError as e:
            print(f"错误：在Linux系统上缺少必要的依赖。请运行 'pip install keyboard Pillow PyQt5' 和 'sudo apt-get install python3-xlib': {e}")
            sys.exit(1)

    # 修改start_hotkey_listener方法中的相关代码
    def start_hotkey_listener(self, hotkey, start_func, block_hotkey=False):
        print("Starting...")
        print(f"监听热键: {hotkey}")
        print("请按下热键来触发功能...")
        
        # 保存热键和回调函数
        self.hotkey = hotkey
        self.start_func = start_func
        self.block_hotkey = block_hotkey
        
        # 重置状态变量
        self.is_processing = False
        self.last_trigger_time = 0
        
        # 设置运行标志
        self.running = True
        
        def on_hotkey_press():
            # 获取当前时间
            current_time = time.time()
            
            # 如果距离上次触发时间太短或已经在处理中，直接返回
            if current_time - self.last_trigger_time < self.TRIGGER_INTERVAL or self.is_processing:
                return
            
            # 设置处理标记
            self.is_processing = True
            self.last_trigger_time = current_time
            
            try:
                # 调用传入的函数
                print(f"热键 {hotkey} 被触发，执行回调函数")
                start_func()
            except Exception as e:
                print(f"执行功能时出错: {e}")
            finally:
                # 确保无论如何都会重置处理标记
                self.is_processing = False
        
        # 保存回调函数引用
        self.on_hotkey_press = on_hotkey_press
        
        # 在新线程中运行热键监听，避免阻塞主线程
        def run_listener():
            try:
                # 注册热键
                self._register_hotkey()
                
                # 开始监听键盘事件
                while self.running:
                    time.sleep(0.1)  # 防止CPU占用过高
                
            except KeyboardInterrupt:
                print("热键监听已停止")
            except Exception as e:
                print(f"热键监听错误: {e}")
            finally:
                # 清理热键注册
                self._remove_hotkey()
                print("热键监听线程已退出")
        
        # 启动监听线程
        self.listener_thread = threading.Thread(target=run_listener, daemon=True)
        self.listener_thread.start()
        
        # 主线程继续执行，等待用户中断
        try:
            # 保持主线程运行
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("程序已被用户中断")
        finally:
            # 停止热键监听
            self.running = False
            if self.listener_thread and self.listener_thread.is_alive():
                self.listener_thread.join(timeout=1.0)
            print("程序已退出")
    
    def adapt_hotkey_for_linux(self, hotkey):
        """在Linux上适配热键（保持原样）"""
        # Linux使用标准的热键命名，不需要特殊转换
        return hotkey
    
    def copy_png_bytes_to_clipboard(self, png_bytes):
        """将PNG字节数据复制到Linux剪贴板"""
        # 这部分代码保持不变
        try:
            # 在Linux上使用不同的剪贴板设置方式
            import subprocess
            import tempfile
            import os
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                f.write(png_bytes)
                temp_filename = f.name
            
            # 使用系统命令将图片复制到剪贴板
            # 对于GNOME桌面环境
            subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', temp_filename])
            
            # 清理临时文件
            os.unlink(temp_filename)
            
        except Exception as e:
            print(f"复制PNG到剪贴板失败: {e}")
            # 如果失败，回退到原来的PyQt5方法
            try:
                clipboard = self.app.clipboard()
                image = QImage.fromData(png_bytes)
                clipboard.setImage(image)
            except Exception:
                pass

    def send_keystroke(self, key_combo):
        """Linux 键盘模拟实现 - 使用keyboard库"""
        try:
            # 解析热键组合，支持多个修饰键
            key_combo = key_combo.lower()
            
            # 为了避免与监听热键冲突，先临时移除热键注册
            self._remove_hotkey()
            
            # 使用keyboard库的press_and_release方法直接发送热键组合
            self.keyboard.press_and_release(key_combo)
            
            time.sleep(0.05)  # 短暂延迟确保按键被正确处理
            
            # 重新注册热键
            if self.running:
                self._register_hotkey()
        except Exception as e:
            print(f"发送键盘事件失败: {e}")
            # 发生错误也要尝试重新注册热键
            if self.running:
                self._register_hotkey()
    
    def try_get_image(self):
        """尝试从Linux剪贴板获取图像"""
        # 这部分代码保持不变
        try:
            clipboard = self.app.clipboard()
            mime_data = clipboard.mimeData()
            
            # 检查剪贴板中是否有图像数据
            if mime_data.hasImage():
                # 获取QPixmap
                pixmap = clipboard.pixmap()
                if not pixmap.isNull():
                    # 将QPixmap转换为QImage
                    q_image = pixmap.toImage()
                    
                    # 将QImage转换为PIL Image
                    buffer = QBuffer()
                    buffer.open(QIODevice.WriteOnly)
                    q_image.save(buffer, "PNG")
                    pil_image = self.Image.open(io.BytesIO(buffer.data()))
                    return pil_image
        except Exception as e:
            print(f"无法从剪贴板获取图像: {e}")
        return None
    
    def _register_hotkey(self):
        """注册热键"""
        try:
            if self.hotkey and hasattr(self, 'on_hotkey_press') and hasattr(self, 'block_hotkey'):
                # 移除已有的热键注册
                self._remove_hotkey()
                # 注册新的热键
                self.hotkey_id = self.keyboard.add_hotkey(
                    self.hotkey, 
                    self.on_hotkey_press,
                    suppress=self.block_hotkey
                )
                print(f"热键 {self.hotkey} 已重新注册")
        except Exception as e:
            print(f"注册热键失败: {e}")
    
    def _remove_hotkey(self):
        """移除热键注册"""
        try:
            if self.hotkey_id:
                self.keyboard.remove_hotkey(self.hotkey_id)
                self.hotkey_id = None
                print("热键已临时移除")
        except Exception:
            # 忽略移除失败的情况
            pass