

from PyQt5.QtWidgets import QWidget, QTextBrowser, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QFont
from PyQt5.QtCore import Qt, QByteArray, QTimer

import traceback
import xml.etree.ElementTree as ET


class Console_TextBrowser(QWidget):
    '''
    自定义的 QTextBrowser, 其中包含1个 TextBrowser, 6个可以调节 TextBrowser 显示的按钮
    6个按钮分别为: 向上, 向下, 增加字号, 减小字号, 重置字号, 清空

    用户可调用方法: 
        向 TextBrowser 中添加文字
            append_text(text_on_textbrowser: str)-> None
        清空 TextBrowser 显示
            clear(self) -> None
    '''

    def append_text(self, text_on_textbrowser: str) -> None:
        '''
        向 TextBrowser 中的末行添加文字

        参数：
            text_on_textbrowser 增添的内容
        '''
        try:
            self.text_browser.moveCursor(QTextCursor.End)
            self.text_browser.insertPlainText(str(text_on_textbrowser) + "\n")
            self.text_browser.moveCursor(QTextCursor.End)
        except Exception as e:
            if self.__flag_traceback_display:
                e = traceback.format_exc()
            self.text_browser.moveCursor(QTextCursor.End)
            self.text_browser.insertPlainText(str(e) + "\n")
            self.text_browser.moveCursor(QTextCursor.End)

    def clear(self) -> None:
        '''
        清空 TextBrowser 显示
        '''
        self.text_browser.clear()

    def __init__(self, default_font_family='Arial', default_font_size=13, traceback_display=False) -> None:
        super().__init__()
        self.__flag_traceback_display = traceback_display
        self.__DEFAULT_FONT_SIZE = default_font_size
        self.__DEFAULT_FONT_FAMILY = default_font_family
        self.__para_init()
        self.__widget_init()
        self.__layout_init()
        self.__signal_connections()

    def __para_init(self):
        '''
        参数初始化
        '''
        self.__SVG_PB_UP = '''
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="800" height="800" viewBox="0 0 200 200" version="1.1" id="svg1" inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)" sodipodi:docname="向上-白.svg"><sodipodi:namedview id="namedview1" pagecolor="#ffffff" bordercolor="#000000" borderopacity="0.25" inkscape:showpageshadow="2" inkscape:pageopacity="0.0" inkscape:pagecheckerboard="0" inkscape:deskcolor="#d1d1d1" inkscape:document-units="mm" inkscape:zoom="0.72426347" inkscape:cx="461.15815" inkscape:cy="450.8028" inkscape:window-width="1920" inkscape:window-height="1009" inkscape:window-x="2552" inkscape:window-y="210" inkscape:window-maximized="1" inkscape:current-layer="layer1" /><defs id="defs1" /><g inkscape:label="图层 1" inkscape:groupmode="layer" id="layer1"><path id="rect1" style="fill:#878787;stroke:#0c0c0c;stroke-width:3.77952756;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke;stroke-dasharray:none;fill-opacity:1;" d="M 100.27086,36.108553 5.3432274,131.03661 29.323587,155.01738 100.27086,84.070121 171.21812,155.01738 195.1989,131.03661 Z" /></g></svg>'''

        self.__SVG_PB_DOWN = '''
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="800" height="800" viewBox="0 0 200 200" version="1.1" id="svg1" inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)" sodipodi:docname="向下-白.svg"><sodipodi:namedview id="namedview1" pagecolor="#ffffff" bordercolor="#000000" borderopacity="0.25" inkscape:showpageshadow="2" inkscape:pageopacity="0.0" inkscape:pagecheckerboard="0" inkscape:deskcolor="#d1d1d1" inkscape:document-units="mm" inkscape:zoom="0.72426347" inkscape:cx="461.15815" inkscape:cy="450.8028" inkscape:window-width="1920" inkscape:window-height="1009" inkscape:window-x="2552" inkscape:window-y="210" inkscape:window-maximized="1" inkscape:current-layer="layer1" /><defs id="defs1" /><g inkscape:label="图层 1" inkscape:groupmode="layer" id="layer1"><path id="rect1" style="fill:#878787;fill-opacity:1;stroke:#0c0c0c;stroke-width:3.77953;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;stroke-dasharray:none;paint-order:fill markers stroke;" d="M 100.27127,155.01738 195.1989,60.089323 171.21854,36.108553 100.27127,107.05581 29.324007,36.108553 5.3432274,60.089323 Z" /></g></svg>'''

        self.__SVG_PB_INCREASE = '''
        <svg width="800" height="800" viewBox="0 0 200 200" version="1.1" id="svg1" inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)" sodipodi:docname="加号-白.svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"> <sodipodi:namedview id="namedview1" pagecolor="#ffffff" bordercolor="#000000" borderopacity="0.25" inkscape:showpageshadow="2" inkscape:pageopacity="0.0" inkscape:pagecheckerboard="0" inkscape:deskcolor="#d1d1d1" inkscape:document-units="mm" inkscape:zoom="1.0242632" inkscape:cx="378.80888" inkscape:cy="360.74711" inkscape:window-width="1920" inkscape:window-height="1009" inkscape:window-x="2552" inkscape:window-y="210" inkscape:window-maximized="1" inkscape:current-layer="layer1" /> <defs id="defs1" /> <g inkscape:label="图层 1" inkscape:groupmode="layer" id="layer1"> <path id="rect1" style="fill:#878787;stroke:#0c0c0c;stroke-width:3.77953;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke;fill-opacity:1" d="M 84.092285,4.6870117 V 82.616699 H 6.2133789 V 115.68799 H 84.092285 v 77.97558 h 33.071285 v -77.97558 h 78.02588 V 82.616699 H 117.16357 V 4.6870117 Z" /> </g> </svg>'''

        self.__SVG_PB_DECREASE = '''
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="800" height="800" viewBox="0 0 200 200" version="1.1" id="svg1" sodipodi:docname="减号-白.svg" inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)"><sodipodi:namedview id="namedview1" pagecolor="#ffffff" bordercolor="#000000" borderopacity="0.25" inkscape:showpageshadow="2" inkscape:pageopacity="0.0" inkscape:pagecheckerboard="0" inkscape:deskcolor="#d1d1d1" inkscape:document-units="mm" inkscape:zoom="0.72426347" inkscape:cx="396.26464" inkscape:cy="450.8028" inkscape:window-width="1920" inkscape:window-height="1009" inkscape:window-x="2552" inkscape:window-y="210" inkscape:window-maximized="1" inkscape:current-layer="layer1" /><defs id="defs1" /><g inkscape:label="图层 1" inkscape:groupmode="layer" id="layer1"><rect style="fill:#878787;stroke:#0c0c0c;stroke-width:3.77953;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke;fill-opacity:1;" id="rect1" width="188.97638" height="33.070866" x="6.2132087" y="82.11689" /></g></svg>'''

        self.__SVG_PB_RESET = '''
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="800" height="800" viewBox="0 0 200 200" version="1.1" id="svg1" inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)" sodipodi:docname="恢复-白.svg"><sodipodi:namedview id="namedview1" pagecolor="#ffffff" bordercolor="#000000" borderopacity="0.25" inkscape:showpageshadow="2" inkscape:pageopacity="0.0" inkscape:pagecheckerboard="0" inkscape:deskcolor="#d1d1d1" inkscape:document-units="mm" inkscape:zoom="1.0242632" inkscape:cx="222.59904" inkscape:cy="438.85205" inkscape:window-width="1920" inkscape:window-height="1009" inkscape:window-x="2552" inkscape:window-y="210" inkscape:window-maximized="1" inkscape:current-layer="layer1" /><defs id="defs1" /><g inkscape:label="图层 1" inkscape:groupmode="layer" id="layer1"><path id="path4" style="fill:#878787;stroke:#0c0c0c;stroke-width:3.77952756;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke;stroke-dasharray:none;fill-opacity:1;" d="M 105.85254 14.645508 A 85.039368 85.039368 0 0 0 26.004883 71.33252 L 45.47998 64.517578 L 51.944824 82.992676 A 56.692913 56.692913 0 0 1 105.85254 42.992188 A 56.692913 56.692913 0 0 1 162.54541 99.685059 A 56.692913 56.692913 0 0 1 105.85254 156.37793 A 56.692913 56.692913 0 0 1 63.743652 137.07275 L 81.060059 125.17041 L 81.428223 123.19336 L 28.83252 113.48242 L 19.056641 166.06543 L 21.033691 166.43018 L 40.154785 153.28711 A 85.039368 85.039368 0 0 0 105.85254 184.72412 A 85.039368 85.039368 0 0 0 190.8916 99.685059 A 85.039368 85.039368 0 0 0 105.85254 14.645508 z " /></g></svg> '''

        self.__SVG_PB_CLEAR = '''
        <svg width="800" height="800" viewBox="0 0 211.66666 211.66667" version="1.1" id="svg1" inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)" sodipodi:docname="橡皮擦.svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"> <sodipodi:namedview id="namedview1" pagecolor="#ffffff" bordercolor="#000000" borderopacity="0.25" inkscape:showpageshadow="2" inkscape:pageopacity="0.0" inkscape:pagecheckerboard="0" inkscape:deskcolor="#d1d1d1" inkscape:document-units="mm" inkscape:zoom="0.51213161" inkscape:cx="385.64306" inkscape:cy="416.88503" inkscape:window-width="1920" inkscape:window-height="1009" inkscape:window-x="2552" inkscape:window-y="210" inkscape:window-maximized="1" inkscape:current-layer="layer1" /> <defs id="defs1" /> <g inkscape:label="图层 1" inkscape:groupmode="layer" id="layer1"> <path id="rect1" style="fill:#878787;fill-opacity:0.988235;stroke-width:12.7546;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke" d="m 134.72498,3.9109743 c -2.30782,-5e-6 -4.61538,0.884152 -6.38374,2.652516 L 7.8636744,127.04106 c -3.536728,3.53672 -3.536722,9.23136 0,12.76809 L 72.61467,204.56014 c 3 536722,3.53672 9.231362,3.53673 12.76809,0 L 205.86033,84.082576 c 3.53673,-3.536727 3.53672,-9.231368 0,-12.76809 l -64.751,-64.7509957 c -1.76836,-1.768365 -4.07655,-2.652521 -6.38435,-2.652516 z m -93.007583,95.6576067 71.215063,71.215069 -4.26931,4.26931 -5.38165,5.38165 -22.224736,22.22473 c -1.235268,1.23527 -3.375174,1.08409 -4.798075,-0.3388 L 10.102656,136.1645 C 8.6797644,134.74162 8.5285844,132.6017 9.7638524,131.36643 L 37.370232,103.76005 c 0.181357,-0.18136 0.386404,-0.32397 0.601626,-0.44593 z" /> </g> </svg>'''

    def __widget_init(self):
        '''
        控件初始化
        '''
        self.text_browser = QTextBrowser()
        self.text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pb_up = QPushButton()
        self.pb_up.setToolTip('向上')
        self.pb_up.setIcon(self.__icon_setup(self.__SVG_PB_UP))
        self.__pushbutton_hover(self.pb_up, self.__set_pb_hover_icon(self.__SVG_PB_UP))
        self.pb_down = QPushButton()
        self.pb_down.setToolTip('向下')
        self.pb_down.setIcon(self.__icon_setup(self.__SVG_PB_DOWN))
        self.__pushbutton_hover(self.pb_down, self.__set_pb_hover_icon(self.__SVG_PB_DOWN))
        self.pb_font_size_increase = QPushButton()
        self.pb_font_size_increase.setToolTip('增大字号')
        self.pb_font_size_increase.setIcon(self.__icon_setup(self.__SVG_PB_INCREASE))
        self.__pushbutton_hover(self.pb_font_size_increase, self.__set_pb_hover_icon(self.__SVG_PB_INCREASE))
        self.pb_font_size_decrease = QPushButton()
        self.pb_font_size_decrease.setToolTip('缩小字号')
        self.pb_font_size_decrease.setIcon(self.__icon_setup(self.__SVG_PB_DECREASE))
        self.__pushbutton_hover(self.pb_font_size_decrease, self.__set_pb_hover_icon(self.__SVG_PB_DECREASE))
        self.pb_reset = QPushButton()
        self.pb_reset.setToolTip('重置字号')
        self.pb_reset.setIcon(self.__icon_setup(self.__SVG_PB_RESET))
        self.__pushbutton_hover(self.pb_reset, self.__set_pb_hover_icon(self.__SVG_PB_RESET))
        self.pb_clear = QPushButton()
        self.pb_clear.setToolTip('清空')
        self.pb_clear.setIcon(self.__icon_setup(self.__SVG_PB_CLEAR))
        self.__pushbutton_hover(self.pb_clear, self.__set_pb_hover_icon(self.__SVG_PB_CLEAR))
        self.setStyleSheet('''
                                QWidget{
                                    border:1px solid rgba(70, 70, 70, 200);
                                    border-radius: 10px;
                                    background-color:rgb(60, 60, 60);
                                }
                            ''')
        self.text_browser.setStyleSheet('''
                                            border: None;
                                            color: rgb(255, 255, 255);
                                        ''')
        font = QFont()
        font.setFamily(self.__DEFAULT_FONT_FAMILY)
        font.setPixelSize(self.__DEFAULT_FONT_SIZE)
        self.text_browser.setFont(font)
        self.__pb_list = [self.pb_up, self.pb_down, self.pb_font_size_increase, self.pb_font_size_decrease, self.pb_reset, self.pb_clear]
        for pb in self.__pb_list:
            pb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            pb.setMinimumHeight(25)
            pb.setStyleSheet('''
                                QPushButton{
                                    border: None;
                                    background-color: transparent;
                                    max-width: 30px;
                                    min-width: 20px;
                                }
                                QPushButton:hover{
                                    padding-bottom: 5px;
                                }
                            ''')
        self.__timer_up = QTimer(self)
        self.__timer_down = QTimer(self)

    def __layout_init(self):
        '''
        布局初始化
        '''
        layout_pb = QHBoxLayout()
        layout_pb.setContentsMargins(0, 0, 0, 0)
        layout_pb.setSpacing(0)
        layout_pb.addWidget(self.pb_up)
        layout_pb.addWidget(self.pb_down)
        layout_pb.addWidget(self.pb_font_size_increase)
        layout_pb.addWidget(self.pb_font_size_decrease)
        layout_pb.addWidget(self.pb_reset)
        layout_pb.addWidget(self.pb_clear)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 5)
        layout.setSpacing(0)
        layout.addWidget(self.text_browser, stretch=100)
        layout.addLayout(layout_pb, stretch=0)
        self.setLayout(layout)

    def __signal_connections(self):
        '''
        信号连接初始化
        '''
        self.__timer_up.timeout.connect(self.__scrolling_up)
        self.__timer_down.timeout.connect(self.__scrolling_down)
        self.pb_up.pressed.connect(self.__start_scrolling_up)
        self.pb_up.released.connect(self.__stop_scrolling_up)
        self.pb_down.pressed.connect(self.__start_scrolling_down)
        self.pb_down.released.connect(self.__stop_scrolling_down)
        self.pb_reset.clicked.connect(self.__font_size_resize)
        self.pb_font_size_increase.clicked.connect(self.__font_size_increase)
        self.pb_font_size_decrease.clicked.connect(self.__font_size_decrease)
        self.pb_clear.clicked.connect(self.text_browser.clear)

    def __set_pb_hover_icon(self, ori_icon: str):
        '''
        设置按钮悬停时的颜色更改

        参数：
            ori_icon: 原来的 SVG 图标字符串
        '''
        return self.__change_svg_fill_color(ori_icon, '#ffffff')

    def __change_svg_fill_color(self, input_svg_str: str, new_fill_color: str) -> str:
        '''
        更改 svg 中的样式颜色

        参数:
            input_svg_str: str, 输入的 svg 字符串
            new_fill_color: str, 新的颜色, RGB 格式, 注意写 '#'
        '''
        root = ET.fromstring(input_svg_str)
        namespaces = {
            'http://www.w3.org/2000/svg': '',
            'http://www.inkscape.org/namespaces/inkscape': 'inkscape',
            'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd': 'sodipodi',
        }
        for element in root.findall('.//{http://www.w3.org/2000/svg}*'):
            fill = element.get('style')
            if fill and fill.lower() != 'none':
                temp_style_dict = dict(item.split(':') for item in fill.split(';') if ':' in item)
                temp_style_dict['fill'] = new_fill_color
                new_style_str = ';'.join(f'{key}:{value}' for key, value in temp_style_dict.items()) + ';'
                element.set('style', new_style_str)
        for uri, prefix in namespaces.items():
            ET.register_namespace(prefix, uri)
        svg_string = ET.tostring(root, encoding='unicode')
        return svg_string

    def __pushbutton_hover(self, button: QPushButton, hover_icon_svg_str: str):
        '''
        按钮悬停样式改变

        参数:
            button: QPushButton, 按钮
            hover_icon_svg_str: str, 悬停的 SVG 图标字符串
        '''
        button_normal_style = button.icon()

        def on_enter(event):
            button.setIcon(self.__icon_setup(hover_icon_svg_str))
            event.accept()

        def on_leave(event):
            button.setIcon(button_normal_style)
            event.accept()
        button.enterEvent = on_enter
        button.leaveEvent = on_leave

    def __icon_setup(self, icon_code: str) -> QIcon:
        '''
        设置QIcon

        参数:
            icon_code: str, SVG 图标字符串
        '''
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_code.encode()))
        return QIcon(pixmap)

    def __font_size_increase(self):
        '''
        增大字号
        '''
        try:
            font = self.text_browser.font()
            size = font.pixelSize()
            font.setPixelSize(size + 1)
            self.text_browser.setFont(font)
        except Exception as e:
            e = traceback.format_exc()
            self.append_text(e)

    def __font_size_decrease(self):
        '''
        减小字号
        '''
        try:
            font = self.text_browser.font()
            size = font.pixelSize()
            font.setPixelSize(size - 1)
            self.text_browser.setFont(font)
        except Exception as e:
            e = traceback.format_exc()
            self.append_text(e)

    def __font_size_resize(self):
        '''
        重置字号
        '''
        try:
            font = self.text_browser.font()
            font.setPixelSize(self.__DEFAULT_FONT_SIZE)
            self.text_browser.setFont(font)
        except Exception as e:
            e = traceback.format_exc()
            self.append_text(e)

    def __start_scrolling_up(self):
        '''
        向上滚动定时器启动
        '''
        self.__timer_up.start(50)

    def __stop_scrolling_up(self):
        '''
        向上滚动定时器停止
        '''
        self.__timer_up.stop()

    def __start_scrolling_down(self):
        '''
        向下滚动定时器启动
        '''
        self.__timer_down.start(50)

    def __stop_scrolling_down(self):
        '''
        向下滚动定时器停止
        '''
        self.__timer_down.stop()

    def __scrolling_up(self):
        '''
        向上滚动
        '''
        scrollbar = self.text_browser.verticalScrollBar()
        value = scrollbar.value()
        scrollbar.setValue(value-2)

    def __scrolling_down(self):
        '''
        向下滚动
        '''
        scrollbar = self.text_browser.verticalScrollBar()
        value = scrollbar.value()
        scrollbar.setValue(value+2)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    main_window = Console_TextBrowser()
    main_window.append_text(main_window._Console_TextBrowser__SVG_PB_INCREASE)
    main_window.show()
    sys.exit(app.exec_())
