<h1 align="center">
  呆啵宠物  |  DyberPet
</h1>

<p align="center">
  旧版的呆啵宠物 (DyberPet) 是一个基于 PyQt5 的桌面宠物开发框架，现已迁移至 PySide6
</p>

<p align="center">
  <a>
    <img src="https://img.shields.io/github/license/ChaozhongLiu/DyberPet.svg">
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/ChaozhongLiu/DyberPet/total.svg"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" />
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/DyberPet-v0.3.0a-green.svg"/>
  </a>
</p>

<p align="center">
简体中文 | <a href="README_EN.md">English</a>
</p>

⚠️ main branch 于 **10/17/2023** 同步至 PySide6 版本，此分支为 PyQt5 版本的存档   


## 衍生成品导航 

- **呆啵宠物 · 原神**：[项目主页](https://github.com/ChaozhongLiu/DyberPet_GenshinImpact) ｜ [B站视频](https://www.bilibili.com/video/BV1fd4y1W7ht)
- **呆啵宠物 · 乃琳**：[微博介绍](https://m.weibo.cn/2765930401/4869193126380684) ｜ [B站视频](https://www.bilibili.com/video/BV1qe4y1F7or)


## 快速体验 Demo
### Windows 用户
  将 Release 下载至本地，双击 **``run_DyberPet.exe``** 即可


### Windows Terminal
  建议首先在本地创建新的 **conda** 环境  
  ```
  conda create --name Dyber_Fluent python=3.9
  conda activate Dyber_Fluent
  conda install -c conda-forge apscheduler
  conda install -c conda-forge pynput
  pip install PyQt-Fluent-Widgets -i https://pypi.org/simple/
  pip install tendo
  ```
  将仓库下载至本地，之后运行 **``run_DyberPet.py``** 即可

  
### MacOS 用户
  建议首先在本地创建新的 **conda** 环境  
  ```
  conda create --name Dyber_Fluent python=3.9
  conda activate Dyber_Fluent
  conda install -c conda-forge apscheduler
  pip install pynput==1.7.6
  pip install PyQt-Fluent-Widgets -i https://pypi.org/simple/
  pip install tendo
  ```
  将仓库下载至本地，之后运行 **``run_DyberPet.py``** 即可


## 用户手册
请参考用户手册，体验现有功能 (施工中)




## 开发者文档
### 素材开发
若您想要在现有功能下，开发一套新的宠物形象、动作，请参考[素材开发文档](docs/art_dev.md)

### 功能开发
若您想要在现有模块下，开发新的功能，请参考[功能开发文档](README.md) (施工中)


## 更新日志

<details>
  <summary>版本更新列表</summary>
  
**  **

**v0.3.0a - 09/24/2023**
- 添加了系统及 UI
  - 基本设置 UI：替换了原本的设置，更贴近 Windows11；增加了语言切换设置
  - 存档管理 UI：实装了存档系统，包括存档的导出、导入，快速存档功能
  - 角色管理 UI：显示角色列表，包含启动按钮、角色信息卡片
- 存档系统改动
  - 存档改动为每个角色独立
  - 添加了新旧存档的自动转换代码
  - 添加了存档文件的各种操作（详见 [添加了系统及 UI]）
- 语言切换
  - 完成了语言切换功能
  - 新增了语言切换相关的文件：``langs.pro``, ``res/language``
  - 部分完成了中英两种语言的翻译
- 重构了原有 UI
  - 利用 PyQt5 原生功能重新实现 按分辨率和缩放改变大小
  - 优化了菜单 UI，替换为 PyQt-Fluent-Widgets RoundMenu
  - 将状态栏移动到了右键菜单中
  - 开启计划任务时，进度条会持续出现在宠物上方
  - 替换了通知窗口的关闭按钮
- 角色添加功能
  - 角色管理UI基本完成
  - 实现了角色添加的基本功能

  
**v0.2.2 - 03/14/2023**
- 数据存写大概花费0.43ms，有极小概率在该间隔内关闭软件导致数据丢失。本次优化在每次关闭前主动存储一次数据，并冻结数据，执行退出。
  
**v0.2.2 - 03/09/2023**
- 可以客制化番茄钟了
- 修复了狂爆物品的另一个大bug
  
**v0.2.2 - 03/08/2023**
- Mac不兼容通知栏关闭按钮，故优化了关闭按钮UI
  
**v0.2.2 - 03/07/2023**
- 附件动作的``follow_mouse``属性添加了``"x"`` 和 ``"y"``的选项，可单独跟随x或y轴
  
**v0.2.2 - 03/05/2023**
- 常驻动作数据结构修改，bug修复
- 同伴添加了常驻动作判定，需要在是主宠物时进行设定
  
**v0.2.2 - 03/04/2023**
- 添加了下落的前置动作``prefall``，将在鼠标松开后执行
- 背包分成了食物和收藏品两栏
  
**v0.2.2 - 03/03/2023**
- 右键菜单中增加了常驻动作选项，可以改变闲置时的默认动作，选中后将不在随机播放其他动作
  
**v0.2.2 - 03/02/2023**
- 交互功能添加了水平跟随目标的功能
- 添加了跟随鼠标的功能
- 目标跟随需要在``pet_conf.json``中定义``left``向左移动和 ``right``向右移动的动作
  
**v0.2.2 - 03/01/2023**
- 存档系统初步功能上线
  
**v0.2.1 - 02/25/2023**
- ``fv_reward``属性可设置为list，物品可出现在多个等级奖励中
  
**v0.2.1 - 02/23/2023**
- Windows系统添加了subwindow属性
- 禁用掉落时，缩放宠物不会闪回地面
  
**v0.2.1 - 02/22/2023**
- 优化了缩放机制
- 物品数量为1时不显示数字
- 优化了主宠物列表判断和默认宠物的保存方式
  
**v0.2.0 - 02/21/2023**
- MacOS 兼容性代码改进
- 增加好感度等级奖励的补偿系统
  
**v0.2.0 - 02/18/2023**
- 设置中添加了启动默认角色的选择
- 切换角色增加了问候通知
- 添加了 NoDropShadowWindowHint （为MacOS准备）
  
**v0.1.19 - 02/16/2023**
- 设置中可以静音了
- 添加了统计陪伴天数及显示铭牌的功能
  
**v0.1.18 - 02/12/2023**
- 对话框自动添加上一步按钮
- 调整了对特殊中文字符的长度计算
  
**v0.1.18 - 02/11/2023**
- 增加了附属宠物和主宠物的连接
- 保证收藏品在随机掉落中不重复出现
- 整理了可变更的系统数值
  
**v0.1.18 - 02/10/2023**
- 添加了对话界面和功能（暂未实装素材）
  
**v0.1.17 - 02/05/2023**
- 给通知系统语音添加了优先级``sound_priority``属性
- 增加了点击时的随机语音事件
- 增加了纳西妲的语音库
  
**v0.1.16 - 02/01/2023**
- 实现了多屏之间转移（测试中）
- 规避了专注时间0分0秒相关的闪退bug
- 解决了不能言说的狂爆物品惊天大bug
- 停止按钮按下后会立刻失效，避免多次结算
- 修复了快速点击鼠标微小位移造成闪现的bug
- 修复了召唤同伴放大时显示不全的问题
- 修复了一定条件下缩放宠物派蒙位置问题
  
**v0.1.15 - 01/29/2023**
- 取消屏幕缩放对图片大小的影响
- 重力加速度最小值变为0.01
- 数值栏字体固定为Times
- 设置内添加是否置顶的选项
  
**v0.1.14 - 01/28/2023**
- 修复了禁用掉落时不会触发摸摸事件的bug
- ``pets.json``转移到了``res/role/``
  
**v0.1.14 - 01/23/2023**
- ``item_config``更新
  - 添加了``fv_reward``: int，将物品设定为好感度升级奖励
  - 修复了label anchor未随缩放比例改变的bug
  - 重力加速度最小值变为0.01
  - 取消屏幕缩放比例对图片大小的影响
  
**v0.1.14 - 01/22/2023**
- ``pet_config['acc_act']``更新
  - ``timeout``：true/false 动画结束后关闭 / 不断循环
  - ``unique``：true/false 可否存在多个一样的附件
  - ``closable``：true/false 可否关闭（右键菜单关闭）
  - ``follow_main``：true/false 是否跟随主程序移动
  - ``speed_follow_main``：int 跟随主程序的移动速度
  
**v0.1.13 - 01/21/2023**
- 优化了widget size的动态变化逻辑
- 修复了没有随机动作或随机动作概率为零时的报错
- 通知栏边框变为圆弧
- 饱食度下降间隔变为 2min
- ``pet_config`` 更新
  - 添加了``subpet``，用来定义宠物的附属宠物
  - ``item_favorite``, ``item_dislike`` 变更为``dict``, 增加了物品好感度倍率数值
- ``item_config``更新
  - 添加了``type``, 可添加消耗品``consumable``和收藏品``collection``两类物品，收藏品不可使用
- ``act_config``更新
  - 添加了``anchor``属性，将根据锚点自动移动动画
- 开始施工语言更换
  
**v0.1.12 - 01/15/2023**
- 待机动作（default）将持续进行
- 更改了数值模块的逻辑，目前所有宠物共用一套数值
  - 删除了``pet_config``中的 ``gravity``, ``hp_interval``, ``fv_interval``
- 进程多开被禁止，以防数据存储混乱
- 多开禁止的情况下，为了能够让多个宠物同屏，增加了``召唤同伴``的功能
- 增加了鼠标点击触发的``摸摸事件``，宠物可定义摸摸的动作，并大概率触发向上浮动的心心，小概率获得物品掉落
- 增加了物品掉落的动画，掉落物品呈抛物线掉落在底部任务栏

**v0.1.11 - 01/07/2023**
- 添加了设置界面，可以改变大小、重力、拖拽速度、音量
- 添加了组件动作：现在支持动作包含另一个动画的功能（具体见素材开发文档）
- 物品使用添加了宠物喜爱度的分级，可设置不同的声音、动作
- 支持宠物自定义通知图标和声音，在``res/role/NAME/note/`` 中添加 （具体见素材开发文档）
- 宠物移动行为增加了屏幕边界
  
**v0.1.10 - 12/28/2022**
- 通知栏的图标和声音与 note_type 关联，可在 ``res/role/PETNAME/note/note_config.json`` 中自定义
  
**v0.1.10 - 12/27/2022**
- 更新了提醒事项的 UI
- 更新了饱食度随时间下降的计算逻辑，每一分钟都会变化，但只显示百分比，与用户定义的 ``hp_interval`` 相关
  
**v0.1.9 - 12/25/2022**
- 更新了番茄钟和专注时间的 UI
- 番茄钟和专注时间的开始和取消移动到了各自的界面内，不再使用菜单进行
- 专注时间可以暂停了
- 专注时间取消也会按已经行的时长获取物品奖励
  
**v0.1.8 - 12/21/2022**
- 界面大小加入了屏幕缩放比例的考虑
- UI 仍然没有全部完成
- 加入了圣诞限定小猫角色
  
**v0.1.8 - 12/19/2022**
- 交互模块QTimer变为更加精准的Timer
  
**v0.1.8 - 12/18/2022**
- 数值系统更新：健康值和心情值替换为 饱食度、好感度，并更新了数值系统及其 UI
- 增加了更多模块连接
  - 数值改变将影响随即动作的触发几率、每个动作的具体概率
  - 动作和物品将伴随好感度提升解锁
  - 更多细节将在用户手册和素材开发文档中更新
- 下落动作细分为 下落中 + 落地动作 两个部分
- 更新了背包系统的 UI，后续将逐渐更新所有的 UI 界面
  
**v0.1.7 - 12/11/2022**
- 添加了计划任务完成后的物品掉落事件

**v0.1.7 - 12/10/2022 (大的来了)**
- 添加了背包系统，可以使用宠物获得的物品（目前只是功能测试阶段，UI极其丑陋，甚至不一致）
  - 在 settings 中增加了 pet_data，用来存储宠物数值和物品的数据
  - 添加了 item_data 和 ``res/items/item_config.json``，用于素材开发中设定物品属性（素材开发文档待更新）
  - 完善了背包交互的一系列可能行为的系统反馈，尽可能考虑了各种情况（可能仍然有bug）
  - 连接了物品使用与数值变化、动画播放
- 添加了通知系统，将取代旧版本中的对话框
  - 定义了 QToaster class 及目前定义的通知类型字段
  - 通知消息会伴随喵叫声
  - 为物品使用和数值变化添加了通知
  - 为计划任务添加了通知，删除了对话框显示（代码仍然在）

**v0.1.6 - 12/03/2022**
- 添加了提醒事项的到时提醒
- 添加了间隔提醒功能
- 关闭宠物后，备忘录会保留
- 添加了对话显示的排队系统，避免冲突

**v0.1.6 - 12/02/2022**
- 添加了专注时间功能
- 添加了番茄时钟和专注时间的倒计时
- 添加了提醒事项（备忘录）
- 该版本下，健康和心情会不断下降，暂时没有和其他功能连接，会在后续版本中添加

**v0.1.5 - 11/27/2022**
- 解决了使用 ``apscheduler`` 时 ``pyinstaller`` 的 bug
- 添加了番茄时间功能

**v0.1.5 - 11/26/2022**
- 采用 ``apscheduler`` 规范化了计划任务模块
- 增加了宠物数值相关数据的读取、修改、存储系统
- 重构了文件夹结构

**v0.1.5 - 11/25/2022**
- 增加了对话框和显示对话的功能
- 增加了计划任务模块
- 计划任务模块增加任务：运行时打招呼、健康和心情随时间下降

**v0.1.4 - 11/23/2022**
- 增加了心情数值
- 更新了呆啵宠物的图标

**v0.1.4 - 11/20/2022**
- 增加了鼠标停留时数值系统的显示 （未实装功能）

**v0.1.3 - 11/19/2022**
- 模块化重构了项目代码

**v0.1.2 - 11/14/2022**
- 最初版本上线


</details>

## 致谢
- Demo 中的部分素材来自 [daywa1kr](https://github.com/daywa1kr/Desktop-Cat)
- 框架早期的动画模块的逻辑参考了 [yanji255](https://toscode.gitee.com/yanji255/desktop_pet/)  
- 框架拖拽掉落的计算逻辑参考了 [WolfChen1996](https://github.com/WolfChen1996/DesktopPet)
