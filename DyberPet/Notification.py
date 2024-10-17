import sys
from sys import platform
import re
import time
import math
import uuid
import types
import random
import inspect
from typing import List
from datetime import datetime, timedelta

from apscheduler.schedulers.qt import QtScheduler
from apscheduler.triggers import interval, date, cron

from PySide6.QtWidgets import *
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtCore import Qt, QTimer, QObject, QPoint, QUrl, QRect, QSize, QPropertyAnimation, QAbstractAnimation
from PySide6.QtGui import QImage, QPixmap, QIcon, QCursor, QColor, QPainter
from PySide6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput

from qfluentwidgets import TextWrap, TransparentToolButton, BodyLabel
from qfluentwidgets import FluentIcon as FIF

from DyberPet.utils import *
from DyberPet.conf import *

import DyberPet.settings as settings

basedir = settings.BASEDIR

##############################
#          通知模块
##############################
'''
通知类型：
1. 系统通知
    字段：system
    图标：DyberPet icon

2. 数值相关通知
    字段：status_{hp, fv, coin}
    图标：hp icon, fv icon, coin icon

3. 计时相关通知
    字段：{start/end/cancel}_{tomato/focus}
    图标：tomato icon, timer icon

4. 物品数量变化通知
    字段：item
    图标：item icon

5. 喂食通知
    字段：feed_{1,2,3}
    图标: item icon

6. 问好
    字段: greeting_{1,2,3,4}
    图标: system
'''


class DPNote(QWidget):

    noteToLog = Signal(QPixmap, str, name="noteToLog")
    send_main_movement = Signal(int, int, name="send_main_movement")

    def __init__(self, parent=None):
        """
        通知组件
        """
        super(DPNote, self).__init__(parent)

        self.items_data = ItemData(HUNGERSTR=settings.HUNGERSTR, FAVORSTR=settings.FAVORSTR)
        sys_note_conf = dict(json.load(open(os.path.join(basedir, 'res/icons/note_icon.json'), 'r', encoding='UTF-8')))
        try:
            pet_note_conf = dict(json.load(open(os.path.join(basedir, 'res/role/{}/note/note.json'.format(settings.petname)), 'r', encoding='UTF-8')))
        except:
            pet_note_conf = {}
        self.icon_dict, self.sound_dict = self.init_note(sys_note_conf, pet_note_conf)
        pet_cof = dict(json.load(open(os.path.join(basedir, 'res/role/{}/pet_conf.json'.format(settings.petname)), 'r', encoding='UTF-8')))
        self.item_favorite = pet_cof.get('item_favorite', [])
        self.item_dislike = pet_cof.get('item_dislike', [])

        self.note_in_prepare = False
        self.bubble_in_prepare = False
        self.note_dict = {}
        self.bubble_dict = {}
        self.height_dict = {}
        self.bb_height_dict = {}
        self.type_dict = {}
        self.sound_playing = []

        if platform == 'win32':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        else:
            # SubWindow not work in MacOS
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        

    def init_note(self, sys_note_conf, pet_note_conf):
        note_config = {}
        sound_config = {}
        for k, v in sys_note_conf.items():
            if k in pet_note_conf.keys():
                if 'image' in pet_note_conf[k].keys():
                    img_file = os.path.join(basedir, 'res/role/{}/note/{}'.format(settings.petname, pet_note_conf[k]['image']))
                else:
                    img_file = os.path.join(basedir, 'res/icons/{}'.format(sys_note_conf[k].get('image', 'icon.png')))

                if 'sound' in pet_note_conf[k].keys():
                    url = os.path.join(basedir, 'res/role/{}/note/{}'.format(settings.petname, pet_note_conf[k]['sound'])) #QUrl.fromLocalFile('res/role/{}/note/{}'.format(settings.pet_data.petname, pet_note_conf[k]['sound']))
                else:
                    url = os.path.join(basedir, 'res/sounds/{}'.format(sys_note_conf[k].get('sound', 'Notification.wav'))) #QUrl.fromLocalFile('res/sounds/{}'.format(sys_note_conf[k].get('sound', '13945.wav')))

                if 'sound_priority' in pet_note_conf[k].keys():
                    pty = pet_note_conf[k]['sound_priority']
                else:
                    pty = sys_note_conf[k].get('sound_priority', 0)

                if 'fv_lock' in pet_note_conf[k].keys():
                    flk = pet_note_conf[k]['fv_lock']
                else:
                    flk = sys_note_conf[k].get('fv_lock', 0)
            else:
                img_file = os.path.join(basedir, 'res/icons/{}'.format(sys_note_conf[k].get('image', 'icon.png')))

                url = os.path.join(basedir, 'res/sounds/{}'.format(sys_note_conf[k].get('sound', 'Notification.wav')))  #QUrl.fromLocalFile('res/sounds/{}'.format(sys_note_conf[k].get('sound', '13945.wav')))

                pty = sys_note_conf[k].get('sound_priority', 0)
                flk = sys_note_conf[k].get('fv_lock', 0)

            note_config[k] = {'image':_load_item_img(img_file), 'sound':url, 'fv_lock':flk}

            if url in sound_config.keys():
                pass
            else:
                sound_config[url] = {'sound':_load_item_sound(url), 'priority': pty}

        for k, v in pet_note_conf.items():
            if k in note_config.keys():
                continue

            if 'image' in pet_note_conf[k].keys():
                img_file = os.path.join(basedir, 'res/role/{}/note/{}'.format(settings.petname, pet_note_conf[k]['image']))
            else:
                img_file = os.path.join(basedir, 'res/icons/icon.png')

            if 'sound' in pet_note_conf[k].keys():
                url = os.path.join(basedir, 'res/role/{}/note/{}'.format(settings.petname, pet_note_conf[k]['sound']))
            else:
                url = os.path.join(basedir, 'res/sounds/Notification.wav')

            if 'sound_priority' in pet_note_conf[k].keys():
                pty = pet_note_conf[k]['sound_priority']
            else:
                pty = 0

            flk = pet_note_conf[k].get('fv_lock', 0)

            note_config[k] = {'image':_load_item_img(img_file), 'sound':url, 'fv_lock':flk}

            if url in sound_config.keys():
                pass
            else:
                sound_config[url] = {'sound':_load_item_sound(url), 'priority': pty}

        return note_config, sound_config #{'image':image, 'sound':player}

    def change_pet(self):
        sys_note_conf = dict(json.load(open(os.path.join(basedir, 'res/icons/note_icon.json'), 'r', encoding='UTF-8')))
        try:
            pet_note_conf = dict(json.load(open(os.path.join(basedir, 'res/role/{}/note/note.json'.format(settings.petname)), 'r', encoding='UTF-8')))
        except:
            pet_note_conf = {}
        self.icon_dict, self.sound_dict = self.init_note(sys_note_conf, pet_note_conf)

        pet_cof = dict(json.load(open(os.path.join(basedir, 'res/role/{}/pet_conf.json'.format(settings.petname)), 'r', encoding='UTF-8')))
        self.item_favorite = pet_cof.get('item_favorite', [])
        self.item_dislike = pet_cof.get('item_dislike', [])


    def setup_notification(self, note_type, message=''):
        # 排队 避免显示冲突
        while self.note_in_prepare:
            time.sleep(1)

        self.note_in_prepare = True

        if note_type in self.icon_dict.keys():
            icon = self.icon_dict[note_type]['image']
            note_type_use = note_type

        elif note_type in self.items_data.item_dict.keys():
            icon = self.items_data.item_dict[note_type]['image']
            note_type_use = 'system'

        elif note_type == 'random':
            random_list = [i for i in self.icon_dict.keys() if i.startswith('random') and\
                           self.icon_dict[i]['fv_lock']<= settings.pet_data.fv_lvl]
            #print(random_list)
            if len(random_list) == 0:
                self.note_in_prepare = False
                return
            else:
                note_type_use = random.sample(random_list,1)[0]
                icon = self.icon_dict[note_type_use]['image']

        else:
            icon = self.icon_dict['system']['image']
            note_type_use = 'system'

        note_index = str(uuid.uuid4())
        if message != '' and settings.toaster_on:
            mergeable_type, merge_num = self.check_note_merge(note_type, message)
        
            if mergeable_type in self.type_dict.keys():
                exist_index, old_value = self.type_dict[mergeable_type]
                new_value = old_value + merge_num
                self.note_dict[exist_index].update_value(new_value)
                self.type_dict[mergeable_type] = (exist_index, new_value)

            else:
                height_margin = sum(self.height_dict.values()) + 10*(len(self.height_dict.keys()))
                self.note_dict[note_index] = DyberToaster(note_index,
                                                        message=message,
                                                        icon=icon,
                                                        corner=Qt.BottomRightCorner,
                                                        height_margin=height_margin,
                                                        closable=True,
                                                        timeout=5000)
                self.note_dict[note_index].closed_note.connect(self.remove_note)
                Toaster_height = self.note_dict[note_index].height()
                self.height_dict[note_index] = int(Toaster_height)

                if mergeable_type:
                    self.type_dict[mergeable_type] = (note_index, merge_num)
        
        self.play_audio(note_type_use, note_index)

        self.note_in_prepare = False
        if message != '':
            self.noteToLog.emit(icon, message)

    def play_audio(self, note_type, note_index):
        # 播放声音
        sound_key = self.icon_dict[note_type]['sound']
        sound_pty = self.sound_dict[sound_key]['priority']

        play_now = False
        
        for i in self.sound_dict.keys():
            if not self.sound_dict[i]['sound'].isPlaying():
                continue
            else:
                played_pty = self.sound_dict[i]['priority']
                if played_pty >= sound_pty:
                    play_now = True
                    break
                else:
                    self.sound_dict[i]['sound'].stop()
                    break
        
        if not play_now:
            self.sound_playing = [note_index, sound_key]
            self.sound_dict[sound_key]['sound'].setVolume(settings.volume)
            self.sound_dict[sound_key]['sound'].play()


    def remove_note(self, note_index, close_type):
        mergeable_note_index = [k for k, v in self.type_dict.items() if v[0] == note_index]
        if mergeable_note_index:
            self.type_dict.pop(mergeable_note_index[0])
        self.note_dict.pop(note_index)
        self.height_dict.pop(note_index)
        if close_type == 'button':
            if note_index == self.sound_playing[0]:
                self.sound_dict[self.sound_playing[1]]['sound'].stop()
        

    def hpchange_note(self, hp_tier, direction):
        # 宠物到达饥饿状态和饿死时，发出通知
        if direction == 'up':
            return
        if hp_tier == 0:
            self.setup_notification('status_hp', message=self.tr('Your pet is starving! (Favor point starts decreasing)'))
        elif hp_tier == 1:
            self.setup_notification('status_hp', message=self.tr('Your pet is hungry now~ (Favor point stops increasing)'))

    def fvchange_note(self, fv_lvl):
        #print(fv_lvl,'note')
        if fv_lvl == -1:
            self.setup_notification('status_fv',
                                    message=self.tr('Congrats! You have reached the max FV level! Thank you for your companionship all this time!'))
        else:
            self.setup_notification('status_fv',
                                    message=f"{self.tr('Favor leveled up:')} lv{int(fv_lvl)}! {self.tr('More features have been unlocked!')}")
            
    def check_note_merge(self, note_type, message):
        direction, merge_num = extract_change_info(message)
        if not direction:
            return None, None
        
        # check type of note
        if note_type in ['status_hp', 'status_fv', 'status_coin'] or note_type in self.items_data.item_dict.keys():
            mergeable_type = f'{note_type}_{direction}'
            
        else:
            return None, None
        
        return mergeable_type, merge_num
    
    def setup_bubbleText(self, bubble_dict, pos_x, pos_y):
        # 排队 避免显示冲突
        while self.bubble_in_prepare:
            time.sleep(1)

        self.bubble_in_prepare = True

        note_index = str(uuid.uuid4())
        message = bubble_dict['message']
        sound_type = bubble_dict.get('sound_type', None)
        icon = bubble_dict.get('icon', None)
        
        # Determine reading time
        if bubble_dict.get("countdown", None):
            timeout = bubble_dict["countdown"]*1000
            countdown = True
        elif bubble_dict.get("timeout", None):
            timeout = bubble_dict["timeout"]*1000
            countdown = False
        else:
            timeout = max(2000, int(1.2 * 1000 * reading_time(message)))
            countdown = False

        # Get note_type for icon and sound
        if not icon:
            icon = None

        elif icon in self.icon_dict.keys():
            icon = self.icon_dict[icon]['image']

        elif icon in self.items_data.item_dict.keys():
            icon = self.items_data.item_dict[icon]['image']

        else:
            icon = None
        height_margin = sum(self.bb_height_dict.values()) + 5*(len(self.bb_height_dict.keys()))
        self.bubble_dict[note_index] = BubbleText(note_index,
                                pos_x, pos_y,
                                height_margin=height_margin,
                                message=message,
                                icon=icon,
                                timeout=timeout,
                                countdown = countdown)
        self.bubble_dict[note_index].closed_bubble.connect(self.remove_bubble)
        self.send_main_movement.connect(self.bubble_dict[note_index].move_to_main)
        bubble_height = self.bubble_dict[note_index].height()
        self.bb_height_dict[note_index] = int(bubble_height)
        
        if sound_type:
            self.play_audio(sound_type, note_index)

        if message != '':
            self.noteToLog.emit(icon, message)
        
        self.bubble_in_prepare = False

    def remove_bubble(self, note_index):
        self.bubble_dict.pop(note_index)
        self.bb_height_dict.pop(note_index)
            



def extract_change_info(message):
    # Regular expression pattern to match the change direction (+ or -) and the value
    pattern = r'([+-])(\d+)'
    
    # Find matches in the message string
    match = re.search(pattern, message)
    
    if match:
        direction = match.group(1)  # + or -
        value = int(match.group(2))  # numerical value
        return direction, value
    else:
        return None, None  # No match found



class DyberToaster(QFrame):
    closed_note = Signal(str, str, name='closed_note')

    def __init__(self, note_index,
                 message='', #parent
                 icon=FIF.INFO,
                 corner=Qt.BottomRightCorner,
                 height_margin=10,
                 closable=True,
                 timeout=5000,
                 parent=None):
        super().__init__(parent=parent)

        self.note_index = note_index
        self.message = message
        self.icon = icon
        self.corner = corner
        self.height_margin = height_margin
        self.isClosable = closable
        self.timeout = timeout
        self.margin = int(10)
        self.close_type = 'faded'
        
        # Duration and Animation
        self.timer = QTimer(singleShot=True, timeout=self.hide)
        self.opacityAni = QPropertyAnimation(self, b'windowOpacity')
        self.opacityAni.setStartValue(0.)
        self.opacityAni.setEndValue(1.)
        self.opacityAni.setDuration(100)
        self.opacityAni.finished.connect(self.checkClosed)
        
        self.__initWidget()
        self.__setForShow()

    def __initWidget(self):
        self.contentLabel = BodyLabel(self)
        self.contentLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.contentLabel.setWordWrap(True)
        self.contentLabel.setFixedWidth(150)
        self.contentLabel.setText(self.message)
        
        self.iconWidget =  QLabel()
        self.iconWidget.setFixedSize(int(26), int(26))
        self.iconWidget.setScaledContents(True)
        self.iconWidget.setPixmap(self.icon)

        self.closeButton = TransparentToolButton(FIF.CLOSE, self)
        self.closeButton.setFixedSize(26, 26)
        self.closeButton.setIconSize(QSize(14, 14))
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.closeButton.setVisible(self.isClosable)
        self.closeButton.clicked.connect(self._closeit)

        self.__initLayout()
        self.adjustSize()

    def __initLayout(self):
        frame = QFrame()
        frame.setStyleSheet('''
            QFrame {
                border: 1px solid black;
                border-radius: 6px; 
                background: rgb(255, 255, 255);
            }
            QLabel{
                border: 0px;
                font: 14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                color: black;
                background-color: transparent;
            }
        ''')
        # Layout
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        # add icon to layout
        self.hBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignVCenter | Qt.AlignLeft)
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.hBoxLayout.addItem(spacerItem1)

        # add message to layout
        self.hBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter | Qt.AlignLeft)

        # add close button to layout
        spacerItem2 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.hBoxLayout.addItem(spacerItem2)
        self.hBoxLayout.addWidget(self.closeButton, 0, Qt.AlignVCenter | Qt.AlignRight)

        frame.setLayout(self.hBoxLayout)
        wholebox = QHBoxLayout()
        wholebox.setContentsMargins(0,0,0,0)
        wholebox.addWidget(frame)
        self.setLayout(wholebox)


    def _closeit(self, close_type='button'):
        if not close_type:
            close_type = 'button'
        self.close_type = close_type
        self.close()

    def checkClosed(self):
        # if we have been fading out, we're closing the notification
        if self.opacityAni.direction() == QAbstractAnimation.Backward: #self.opacityAni.Backward:
            self._closeit('faded')

    def restore(self):
        # this is a "helper function", that can be called from mouseEnterEvent
        # and when the parent widget is resized. We will not close the
        # notification if the mouse is in or the parent is resized
        self.timer.stop()
        # also, stop the animation if it's fading out...
        self.opacityAni.stop()
        # ...and restore the opacity
        self.setWindowOpacity(1)

    def hide(self):
        # start hiding
        self.opacityAni.setDirection(QAbstractAnimation.Backward)
        self.opacityAni.setDuration(500)
        self.opacityAni.start()

    def enterEvent(self, event):
        self.restore()

    def leaveEvent(self, event):
        self.timer.start()

    def closeEvent(self, event):
        # we don't need the notification anymore, delete it!
        self.closed_note.emit(self.note_index, self.close_type)
        self.deleteLater()

    def showEvent(self, e):
        super().showEvent(e)
        self.adjustSize()

    def __setForShow(self):
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        if platform == 'win32':
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
            Qt.BypassWindowManagerHint | Qt.SubWindow | Qt.NoDropShadowWindowHint)
        else:
            # SubWindow not work in MacOS
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
            Qt.BypassWindowManagerHint | Qt.NoDropShadowWindowHint)

        # get current screen
        parentRect = self._getCurrentRect()

        # raise the widget and adjust its size to the minimum
        self.raise_()
        self.adjustSize()

        # Note position
        self.height_margin = int(self.height_margin) #*size_factor)
        geo = self.geometry()
        if self.corner == Qt.TopLeftCorner:
            geo.moveTopLeft(
                parentRect.topLeft() + QPoint(self.margin, self.margin+self.height_margin))
        elif self.corner == Qt.TopRightCorner:
            geo.moveTopRight(
                parentRect.topRight() + QPoint(-self.margin, self.margin+self.height_margin))
        elif self.corner == Qt.BottomRightCorner:
            geo.moveBottomRight(
                parentRect.bottomRight() + QPoint(-self.margin, -(self.margin+self.height_margin)))
        else:
            geo.moveBottomLeft(
                parentRect.bottomLeft() + QPoint(self.margin, -(self.margin+self.height_margin)))

        self.timer.setInterval(self.timeout)
        self.timer.start()
        self.setGeometry(geo)
        self.show()
        self.opacityAni.start()


    def _getCurrentRect(self):
        currentScreen = QApplication.primaryScreen()
        # reference for the screen
        reference = QRect(QCursor.pos() - QPoint(1, 1), 
                          QSize(3, 3))
        maxArea = 0
        for screen in QApplication.screens():
            intersected = screen.geometry().intersected(reference)
            area = intersected.width() * intersected.height()
            if area > maxArea:
                maxArea = area
                currentScreen = screen
        return currentScreen.availableGeometry()
    
    def update_value(self, new_value):
        self.restore()
        self.update_message_value(new_value)
        self.contentLabel.setText(self.message)
        self.adjustSize()
        self.timer.start()

    def update_message_value(self, new_value):
        # Define the regex pattern to match + or - followed by digits, ensuring it's at the end of the string
        pattern = r'([+-])(\d+)$'
        
        # Use a callback in re.sub to replace the number after + or -
        def replace_match(match):
            sign = match.group(1)  # Get the sign (+ or -)
            # Return the sign followed by the new value as a string
            return f"{sign}{new_value}"
        
        # Replace the matched pattern only if it's at the end of the text
        self.message = re.sub(pattern, replace_match, self.message)


class VerticalSeparator(QWidget):
    """ Vertical separator """

    def __init__(self, color, height=3, parent=None):
        self.color = color
        super().__init__(parent=parent)
        self.setFixedWidth(height)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(self.color)
        painter.drawLine(1, 0, 1, self.height())


class BubbleText(QFrame):
    closed_bubble = Signal(str, name='closed_bubble')

    def __init__(self, note_index,
                 pos_x, pos_y, 
                 height_margin = 0,
                 message='',
                 icon=None,
                 timeout=5000,
                 countdown=False,
                 parent=None):
        super().__init__(parent=parent)

        self.note_index = note_index
        self.message = message
        self.icon = icon
        self.timeout = timeout
        self.leftover = int(timeout/1000)
        self.countdown = countdown
        self.pos_x = pos_x
        self.pos_y = pos_y-settings.current_img.height()-height_margin
        self.height_margin = height_margin
        
        # Duration and Animation
        self.timer = QTimer(singleShot=True, timeout=self.hide)
        self.opacityAni = QPropertyAnimation(self, b'windowOpacity')
        self.opacityAni.setStartValue(0.)
        self.opacityAni.setEndValue(1.)
        self.opacityAni.setDuration(100)
        self.opacityAni.finished.connect(self.checkClosed)

        # Count down timer
        if self.countdown:
            self.countdown_timer = QTimer(timeout=self.update_countdown)
        
        self.__initWidget()
        self.__setForShow()

    def __initWidget(self):
        if self.message:
            self.contentLabel = BodyLabel(self)
            self.contentLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.contentLabel.setWordWrap(True)
            self.contentLabel.setText(self.message)
        
        if self.icon:
            self.iconWidget =  QLabel()
            self.iconWidget.setFixedSize(int(18), int(18))
            self.iconWidget.setScaledContents(True)
            self.iconWidget.setPixmap(self.icon)
        else:
            self.iconWidget =  None

        if self.countdown:
            self.countdownLabel = BodyLabel(self)
            self.countdownLabel.setAlignment(Qt.AlignCenter)
            self.countdownLabel.setWordWrap(False)
            self.countdownLabel.setText(convert_seconds_to_mmss(self.leftover))
        else:
            self.countdownLabel = None

        self.__initLayout()
        self.adjustSize()

    def __initLayout(self):
        frame = QFrame()
        frame.setStyleSheet('''
            QFrame {
                border: 1px solid rgb(0, 0, 0);
                border-radius: 10px;
                background: rgba(255, 255, 255, 220);
            }
            QLabel{
                border: 0px;
                font: 14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                color: rgba(25, 25, 25, 245);
                background-color: transparent;
            }
        ''')
        # Layout
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        # add icon to layout
        if self.iconWidget:
            self.hBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignVCenter | Qt.AlignLeft)
        
        if self.iconWidget and self.message:
            spacerItem1 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.hBoxLayout.addItem(spacerItem1)

        # add message to layout
        if self.message:
            self.hBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignCenter)
        
        if self.countdownLabel:
            spacerItem2 = QSpacerItem(2, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.hBoxLayout.addItem(spacerItem2)
            self.hBoxLayout.addWidget(VerticalSeparator(QColor(20,20,20,175)))
            spacerItem3 = QSpacerItem(2, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.hBoxLayout.addItem(spacerItem3)
            self.hBoxLayout.addWidget(self.countdownLabel, 0, Qt.AlignCenter)

        frame.setLayout(self.hBoxLayout)
        wholebox = QHBoxLayout()
        wholebox.setContentsMargins(0,0,0,0)
        wholebox.addWidget(frame)
        self.setLayout(wholebox)


    def _closeit(self):
        self.close()

    def checkClosed(self):
        if self.opacityAni.direction() == QAbstractAnimation.Backward:
            self._closeit()

    def restore(self):
        # this is a "helper function", that can be called from mouseEnterEvent
        # and when the parent widget is resized. We will not close the
        # notification if the mouse is in or the parent is resized
        self.timer.stop()
        # also, stop the animation if it's fading out...
        self.opacityAni.stop()
        # ...and restore the opacity
        self.setWindowOpacity(1)

    def enterEvent(self, event):
        if not self.countdown:
            self.restore()

    def leaveEvent(self, event):
        if not self.countdown:
            self.timer.start()

    def hide(self):
        # start hiding
        self.opacityAni.setDirection(QAbstractAnimation.Backward)
        self.opacityAni.setDuration(500)
        self.opacityAni.start()

    def closeEvent(self, event):
        self.closed_bubble.emit(self.note_index)
        self.deleteLater()

    def showEvent(self, e):
        super().showEvent(e)
        self.adjustSize()

    def __setForShow(self):
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        if platform == 'win32':
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
            Qt.BypassWindowManagerHint | Qt.SubWindow | Qt.NoDropShadowWindowHint)
        else:
            # SubWindow not work in MacOS
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
            Qt.BypassWindowManagerHint | Qt.NoDropShadowWindowHint)

        # raise the widget and adjust its size to the minimum
        self.raise_()
        self.adjustSize()

        # Note position
        self.move(self.pos_x-self.width()//2, self.pos_y-self.height())

        self.timer.setInterval(self.timeout)
        self.timer.start()
        self.show()
        self.opacityAni.start()
        if self.countdown:
            self.countdown_timer.start(1000)

    def move_to_main(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y-settings.current_img.height()-self.height_margin
        self.move(self.pos_x-self.width()//2, self.pos_y-self.height())

    def update_countdown(self):
        self.leftover -= 1
        self.countdownLabel.setText(convert_seconds_to_mmss(self.leftover))



def _load_item_img(img_path):
    return _get_q_img(img_path)

def _get_q_img(img_file) -> QPixmap:
    image = QPixmap()
    image.load(img_file)
    return image

def _load_item_sound(file_path):
    
    player = QSoundEffect()
    url = QUrl.fromLocalFile(file_path)
    player.setSource(url)
    player.setVolume(settings.volume)
    return player


def reading_time(text: str) -> float:
    # Average reading speeds
    ENGLISH_WPM = 225  # Average words per minute for English
    CHINESE_CPM = 170  # Average characters per minute for Chinese

    # Regex patterns for detecting English words and Chinese characters
    english_words = re.findall(r'[a-zA-Z]+', text)
    chinese_characters = re.findall(r'[\u4e00-\u9fff]', text)

    # Count words and characters
    english_word_count = len(english_words)
    chinese_char_count = len(chinese_characters)

    # Calculate time in seconds for each part
    english_reading_time = (english_word_count / ENGLISH_WPM) * 60
    chinese_reading_time = (chinese_char_count / CHINESE_CPM) * 60

    # Total reading time
    total_reading_time = english_reading_time + chinese_reading_time
    return total_reading_time


def convert_seconds_to_mmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02}:{int(seconds):02}"