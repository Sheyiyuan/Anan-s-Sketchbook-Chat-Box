# 安安的素描本聊天框（MacOS 和 Linux 版本）

本项目是一个将你在一个文本输入框中的文字或图片写到安安的素描本上的项目。

这个项目是 [原项目](https://github.com/MarkCup-Official/Anan-s-Sketchbook-Chat-Box) 的 MacOS 和 Linux 支持版本，随缘更新，不保证功能和原项目同步。

## AI声明

本项目基本上你看得到的的代码都由AI生成

## 部署

本项目支持 MacOS 和 Linux 系统。

理论上支持 Windows 系统，但是我只有理论，没有任何测试的同时功能更新慢，不推荐使用。

现在字体文件和安安图片已经内置于项目中，无需再额外置入DLC。

其中 `font.ttf` 为字体文件，可以自由修改成其他字体，本项目不拥有字体版权，仅做引用。

如果分辨率不一样的安安图片，需要修改 `config.py` 的 `TEXT_BOX_TOPLEFT` 和 `IMAGE_BOX_BOTTOMRIGHT`，定义文本框的大小。

依赖库安装: `pip install -r requirements.txt `

## 使用

使用文本编辑器打开 `config.py` 即可看到方便修改的参数，可以设置热键，图片路径，字体路径等。

运行 `main.py` 即可开始监听设置好的快捷键，按下回车会自动拦截按键，生成图片后自动粘贴（自动发送功能可以在 config.py 中开启）。

如果发送失败等可以尝试适当增大 `config.py` 第46行的 `DELAY` 。

输入`#普通#`, `#开心#`, `#生气#`, `#无语#`, `#脸红#`, `#病娇#`可以切换标签差分, 一次切换一直有效. 可以通过修改`BASEIMAGE_MAPPING`来增加更多差分。

如果发送失败等可以尝试适当增大 `main.py` 第10行的 `DELAY` 。

## 关于 MacOS 系统的说明

> 此处 MacOS 的测试环境为 MacOS Tahoe 26.0.1

如果你在 MacOS 下使用需要使用管理员权限（sudo）运行。

另外，MacOS 由于安全限制，使用了与 Windows 系统下不同的实现。经测试在 QQ 等软件中修饰键和回车一起输入时回车会被吃掉，请自行设置其他快捷键。

推荐快捷键为 `cmd+.`

在使用中文输入法时偶尔会触发输入法而无法调用图片生成的情况，尤其是启动后第一次运行时。该 bug 目前还未解决，一般重试即可，不影响正常使用。

## 关于 Linux 系统的说明

> 此处 Linux 的测试环境为 Arch Linux with Gnome (Wayland)

需要依赖 `xclip` 。

如果你在 Linux 下使用，需要以 root 用户身份运行。

Linux 系统下气球被简易长矛抓走拿去当泡腾片泡茶了，不能图套图。可能是 bug ，但是我不会修。

和 MacOS 一样，经测试在 QQ 等软件中修饰键和回车一起输入时回车会被吃掉，请自行设置其他快捷键。

推荐快捷键为 `ctrl+.`

## 关于 Windows 系统的说明

> 此处 Windows 的测试环境为 Null

理论上是支持 Windows 的，但是我因为没有环境所以没有测试过，建议去用原项目，更新比这边快而且适配更好。

## MacOS 下载后完整食用教程

- 隐私设置

系统设置 -> 隐私与安全性 -> 辅助功能 -> 列表左下的加号 -> 实用工具 -> 终端 -> 允许

- 打开终端

在访达中选中下载好的文件夹 -> 右键 -> 服务 -> 新建位于文件夹位置的终端窗口

然后把下面的命令复制粘贴进去。

- 安装uv

```zsh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- 通过 uv 安装 python 并启用虚拟环境

```zsh
uv venv --python 3.13 .venv
source .venv/bin/activate
```

- 安装依赖

```zsh
uv pip install -r requirements.txt
```

- 运行

```zsh
sudo uv run main.py
```

这里需要输入你电脑的开机密码，密码输入后不会显示，输往回车确认即可。
