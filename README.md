# Pip_Conda_Manager

## 项目开发原因

因为之前使用Anaconda， 在卸载Anaconda时，发现Anaconda将左右的python库，包括本地非虚拟环境的库都删除了，将自己原来的库安装回去比较麻烦，所以写了这个管理器，想要管理所有的库，包括虚拟环境和本地环境



## 软件简介

该软件用于windows系统上python开发环境管理，可以管理虚拟环境以及本地环境。

当用户运行软件时，软件会自动读取计算机中所有的python本地环境以及Conda环境，其他环境可以在启动后手动添加，目前只支持venv。

用户可以在 `虚拟环境管理 `界面中对虚拟环境进行管理。目前仅支持 Conda

在虚拟环境管理中，用户可以新建环境，更新环境，删除环境。其中更新环境不建议使用，因为其运行时间较长，而且至今仍有bug(运行响应时间过长)。如更新环境，建议在主界面中手动选择所有的需要更新项目进行更新(可以在 `批量安装导入` 或者在 `已安装` 中进行选择)

当用户选择环境后，如果用户安装了 `pipdeptree` ， 则可以看到当前 python 环境的依赖项

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/ch_01.png" alt="image1" height = "150" align=center > </div>

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/ch_02.png" alt="image1" height = "150" align=center > </div>

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/ch_03.png" alt="image1" height = "150" align=center > </div>

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/ch_04.png" alt="image1" height = "150" align=center > </div>

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/ch_05.png" alt="image1" height = "150" align=center > </div>

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/en_01.png" alt="image1" height = "150" align=center > </div>

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/en_02.png" alt="image1" height = "150" align=center > </div>

<div style="display:inline-block">  <img src="https://github.com/Jf-JIN/Pip_Conda_Manager/blob/main/img/startup.png" alt="image1" height = "150" align=center > </div>