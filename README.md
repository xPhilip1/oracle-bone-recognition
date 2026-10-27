# 甲骨文字形识别（K210 + ESP8266 + Android）

> 把甲骨文拓片上的字形对准摄像头，屏幕上直接显示它对应的现代汉字。

K210 上跑 YOLOv2 轻量检测模型，识别三类字形（`xiang` / `juzi` / `dong`），在 LCD 上画框并标注置信度，
同时通过串口输出对应的汉字编码；ESP8266 负责联网转发，Android 端（E4A 编写）做展示与调试。

## 功能特性

- **端侧识别**：K210 KPU 推理，QVGA 输入，无需联网即可出结果
- **实时可视化**：LCD 实时画框 + 类别 + 置信度 + FPS
- **串口上报**：识别到目标后输出汉字 Unicode 编码（如 香 / 冻），供下位机或 App 使用
- **联网桥接**：ESP8266 MicroPython 脚本接收串口数据并通过 UDP 转发
- **Android 端**：E4A 工程（摄像头预览 + 结果展示），附带调试版 APK 可直接安装

## 技术栈

| 端 | 技术 |
| --- | --- |
| 视觉 | K210（CanMV / MaixPy）+ KPU + YOLOv2 |
| 联网 | ESP8266 + MicroPython（socket / WLAN） |
| 移动端 | E4A（易安卓） |
| 模型 | `det.kmodel`（3 类，320×240 输入） |

## 目录结构

```
oracle-bone-recognition/
├── K210/
│   ├── main.py        # 屏幕启动画面 + 环境初始化
│   ├── wang2.py       # 主识别脚本：加载 det.kmodel、画框、串口输出
│   ├── boot.py        # 开机自检
│   └── det.kmodel     # 检测模型
├── Thoony(8266)/
│   └── Thoony(8266)/main.py   # ESP8266：连 WiFi、收串口、UDP 转发
├── E4A/
│   ├── 摄像头 - 副本1.e4a      # 安卓工程（E4A 打开）
│   └── 调试版_红线检测.apk      # 可直接安装的调试包
```

## 运行前必须自己准备

| 项 | 说明 |
| --- | --- |
| **K210 + CanMV** | `det.kmodel` 放 SD 卡根目录（代码按 `/sd/det.kmodel` 加载），用 CanMV IDE 运行 `wang2.py` |
| **WiFi 名称与密码** | `Thoony(8266)/Thoony(8266)/main.py` 里的 `YOUR_WIFI_SSID` / `YOUR_WIFI_PASSWORD`，本副本已清空 |
| **ESP8266 固件** | MicroPython 固件 + Thonny 上传脚本 |
| **E4A 环境** | 要改安卓端得装易安卓（E4A）；只想体验就直接装 `调试版_红线检测.apk`（手机允许未知来源） |
| **类别与模型必须对齐** | 换模型时要同步改 `wang2.py` 的 `labels` 与 `anchor`，否则识别结果对不上号 |

## 运行步骤

1. **准备模型**：把 `K210/det.kmodel` 拷到 SD 卡根目录（代码按 `/sd/det.kmodel` 加载）。
2. **烧录视觉端**：CanMV IDE 打开 `K210/wang2.py` 运行；UART2（115200）接 ESP8266。
3. **联网端**：Thonny 打开 `Thoony(8266)/Thoony(8266)/main.py`，先改 WiFi 名称与密码，
   上传后复位；脚本会向固定端口发 UDP 包。
4. **安卓端**：安装 `E4A/调试版_红线检测.apk`，或用 E4A 打开 `.e4a` 工程重新编译。

> 本副本中的 WiFi 账号已替换为占位符，直接运行前必须改成你自己的。

## 模型与识别类别

`wang2.py` 中的类别表：

```python
labels = ["xiang", "juzi", "dong"]          # 三类字形
unicode_map = {"xiang": ord("香"), "dong": ord("冻")}   # 串口输出的汉字
```

换自己的数据集时，只需要替换 `det.kmodel` 并同步修改 `labels` / `anchor`。

## 已知问题

- 只做了 3 类，样本量小，光照变化大时置信度波动明显；
- `unicode_map` 里 `juzi` 没有映射，识别到该类时不会输出汉字（脚本里是 `if label in unicode_map` 保护）；
- `main.py` 只是启动画面，实际入口是 `wang2.py`，两个文件容易混淆；
- APK 是调试签名，安装时需要在手机上允许"未知来源"。

## License

课程/竞赛作品，仅供学习交流。
