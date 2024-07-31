
from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QByteArray

import time


class Manager_Splash_Screen(QSplashScreen):
    def __init__(self):

        self.splash_pix = QPixmap(200, 250)
        self.splash_pix.fill(QColor(251, 246, 226))
        super().__init__(self.splash_pix, Qt.WindowStaysOnTopHint)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.label = QLabel()
        space = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setPixmap(self.pixmap_setup(self.svg_data()))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout_label = QHBoxLayout()
        layout_label.setContentsMargins(0, 0, 0, 0)
        layout_label.setSpacing(0)
        layout_label.addItem(space)
        layout_label.addWidget(self.label)
        layout_label.addItem(space)
        layout.addLayout(layout_label)

        self.showMessage('加载 pip 环境', Qt.AlignBottom | Qt.AlignCenter, QColor(19, 24, 66))
        self.show()

    def pixmap_setup(self, icon_code: str):
        '''
        设置pixmap

        参数:
            Icon_code: SVG 的源码(str)
        '''
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_code.encode()))
        return pixmap

    def close_splash_screen(self, widget):
        self.finish(widget)

    def show_message(self, message: str):
        self.showMessage(str(message), Qt.AlignBottom | Qt.AlignCenter, QColor(19, 24, 66))
        # time.sleep(1)

    def svg_data(self):
        return ''' 
    <svg
   width="157.24979"
   height="193.16484"
   viewBox="0 0 41.605673 51.108198"
   version="1.1"
   id="svg1"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs1">
    <linearGradient
       xlink:href="#linearGradient3"
       id="linearGradient4"
       x1="-65.305511"
       y1="210.47717"
       x2="-35.763237"
       y2="181.33167"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.24553087,-0.29259241,0.24553087,0.29259241,71.452395,97.055245)" />
    <linearGradient
       id="linearGradient3">
      <stop
         style="stop-color:#505050;stop-opacity:1;"
         offset="0.29652995"
         id="stop3" />
      <stop
         style="stop-color:#c88c1e;stop-opacity:1;"
         offset="0.45189276"
         id="stop6" />
      <stop
         style="stop-color:#c88c4b;stop-opacity:1;"
         offset="0.66246057"
         id="stop4" />
    </linearGradient>
    <linearGradient
       xlink:href="#linearGradient17"
       id="linearGradient18"
       x1="80"
       y1="100.74315"
       x2="125"
       y2="100.74315"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.34723309,0,0,0.41378816,71.452395,97.055245)" />
    <linearGradient
       id="linearGradient17">
      <stop
         style="stop-color:#8c541b;stop-opacity:1;"
         offset="0"
         id="stop17" />
      <stop
         style="stop-color:#8b541b;stop-opacity:0.50226247;"
         offset="0.12460568"
         id="stop19" />
      <stop
         style="stop-color:#8c541b;stop-opacity:1;"
         offset="0.24842271"
         id="stop20" />
      <stop
         style="stop-color:#8b541b;stop-opacity:0.50226247;"
         offset="0.40339115"
         id="stop21" />
      <stop
         style="stop-color:#8c541b;stop-opacity:1;"
         offset="0.50374603"
         id="stop22" />
      <stop
         style="stop-color:#8b541b;stop-opacity:0.49773756;"
         offset="0.63278788"
         id="stop23" />
      <stop
         style="stop-color:#8c541b;stop-opacity:1;"
         offset="0.75"
         id="stop24" />
      <stop
         style="stop-color:#8b541b;stop-opacity:0.49547511;"
         offset="0.87310231"
         id="stop25" />
      <stop
         style="stop-color:#8c541b;stop-opacity:1;"
         offset="1"
         id="stop18" />
    </linearGradient>
    <linearGradient
       xlink:href="#linearGradient7"
       id="linearGradient9"
       x1="87.773003"
       y1="180.56271"
       x2="113.05469"
       y2="180.56271"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.97197634,0,0,0.97197634,21.996629,-17.457584)" />
    <linearGradient
       id="linearGradient7">
      <stop
         style="stop-color:#5096b4;stop-opacity:0.73981899;"
         offset="0.18138801"
         id="stop8" />
      <stop
         style="stop-color:#969696;stop-opacity:0.38999999;"
         offset="0.26340693"
         id="stop12" />
      <stop
         style="stop-color:#5096b4;stop-opacity:1;"
         offset="0.40851733"
         id="stop9" />
    </linearGradient>
    <linearGradient
       xlink:href="#linearGradient1"
       id="linearGradient2"
       x1="61.287144"
       y1="81.627716"
       x2="199.64444"
       y2="81.627716"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.97197634,0,0,0.97197634,-9.6844609,-31.517886)"
       spreadMethod="pad" />
    <linearGradient
       id="linearGradient1">
      <stop
         style="stop-color:#f0f0f0;stop-opacity:0.59502262;"
         offset="0.17192426"
         id="stop1" />
      <stop
         style="stop-color:#00c8ff;stop-opacity:0.49773756;"
         offset="0.30914825"
         id="stop3-4" />
      <stop
         style="stop-color:#00c8ff;stop-opacity:0.72624433;"
         offset="0.46687701"
         id="stop4-0" />
      <stop
         style="stop-color:#00c8ff;stop-opacity:0;"
         offset="0.69242901"
         id="stop2" />
    </linearGradient>
    <linearGradient
       xlink:href="#linearGradient5"
       id="linearGradient6"
       x1="93.414001"
       y1="139.10304"
       x2="107.32981"
       y2="139.10304"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.98912679,0,0,0.56938732,20.275201,32.141317)" />
    <linearGradient
       id="linearGradient5">
      <stop
         style="stop-color:#000000;stop-opacity:0.1199095;"
         offset="0.26498422"
         id="stop5" />
      <stop
         style="stop-color:#000000;stop-opacity:0.49803922;"
         offset="0.54100949"
         id="stop7" />
      <stop
         style="stop-color:#000000;stop-opacity:1;"
         offset="1"
         id="stop6-1" />
    </linearGradient>
    <linearGradient
       xlink:href="#linearGradient13"
       id="linearGradient14"
       x1="88.349998"
       y1="220.27213"
       x2="112.4607"
       y2="220.27213"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(0.94765038,0.21609419,-0.21609419,0.94765038,25.327362,-12.130276)" />
    <linearGradient
       id="linearGradient13">
      <stop
         style="stop-color:#505050;stop-opacity:1;"
         offset="0.16246057"
         id="stop13" />
      <stop
         style="stop-color:#505050;stop-opacity:0.44;"
         offset="0.25236592"
         id="stop15" />
      <stop
         style="stop-color:#505050;stop-opacity:1;"
         offset="0.39432177"
         id="stop14" />
    </linearGradient>
  </defs>
  <g
     id="layer1"
     transform="matrix(0.35041351,0,0,0.35041351,-8.0258547,-4.7995597)">
    <g
       id="layer3">
      <rect
         style="fill:#131842;fill-opacity:1;stroke:#003b6e;stroke-width:4.35893;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;stroke-dasharray:none;stroke-opacity:1;paint-order:fill markers stroke"
         id="rect2"
         width="112.14735"
         height="121.83098"
         x="25.083418"
         y="15.87631"
         rx="7.5059795"
         ry="6.5190878" />
      <path
         id="rect1"
         style="fill:#e68369;fill-opacity:0.988235;stroke-width:9.2261;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke"
         d="m 59.178865,26.773628 h 63.014425 c 4.15832,0 7.50599,1.90314 7.50599,4.267129 v 7.071022 c 0,2.36399 -3.34767,4.26713 -7.50599,4.26713 H 59.178865 c -4.15832,0 -7.505993,-1.90314 -7.505993,-4.26713 v -7.071022 c 0,-2.363989 3.347673,-4.267129 7.505993,-4.267129 z m -11.633301,7.961879 a 7.9618771,7.9618771 0 0 1 -7.961877,7.961877 7.9618771,7.9618771 0 0 1 -7.961877,-7.961877 7.9618771,7.9618771 0 0 1 7.961877,-7.961877 7.9618771,7.9618771 0 0 1 7.961877,7.961877 z" />
      <path
         id="rect1-2"
         style="fill:#e68369;fill-opacity:0.988235;stroke-width:9.2261;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke"
         d="m 59.178863,48.568262 h 63.014427 c 4.15832,0 7.50599,1.90314 7.50599,4.267129 v 7.071022 c 0,2.36399 -3.34767,4.26713 -7.50599,4.26713 H 59.178863 c -4.15832,0 -7.505993,-1.90314 -7.505993,-4.26713 v -7.071022 c 0,-2.363989 3.347673,-4.267129 7.505993,-4.267129 z m -11.6333,7.961879 a 7.9618771,7.9618771 0 0 1 -7.961877,7.961877 7.9618771,7.9618771 0 0 1 -7.961877,-7.961877 7.9618771,7.9618771 0 0 1 7.961877,-7.961877 7.9618771,7.9618771 0 0 1 7.961877,7.961877 z" />
      <path
         id="rect1-23"
         style="fill:#e68369;fill-opacity:0.988235;stroke-width:9.2261;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke"
         d="m 59.178863,70.362896 h 63.014427 c 4.15832,0 7.50599,1.90314 7.50599,4.267129 v 7.071022 c 0,2.36399 -3.34767,4.267129 -7.50599,4.267129 H 59.178863 c -4.15832,0 -7.505993,-1.903139 -7.505993,-4.267129 v -7.071022 c 0,-2.363989 3.347673,-4.267129 7.505993,-4.267129 z m -11.6333,7.961879 a 7.9618771,7.9618771 0 0 1 -7.961877,7.961877 7.9618771,7.9618771 0 0 1 -7.961877,-7.961877 7.9618771,7.9618771 0 0 1 7.961877,-7.961877 7.9618771,7.9618771 0 0 1 7.961877,7.961877 z" />
      <path
         id="rect1-8"
         style="fill:#e68369;fill-opacity:0.988235;stroke-width:9.2261;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke"
         d="m 59.178863,92.15753 h 63.014427 c 4.15832,0 7.50599,1.903142 7.50599,4.267128 v 7.071022 c 0,2.36399 -3.34767,4.26713 -7.50599,4.26713 H 59.178863 c -4.15832,0 -7.505993,-1.90314 -7.505993,-4.26713 v -7.071022 c 0,-2.363986 3.347673,-4.267128 7.505993,-4.267128 z m -11.6333,7.96188 a 7.9618771,7.9618771 0 0 1 -7.961877,7.96188 7.9618771,7.9618771 0 0 1 -7.961877,-7.96188 7.9618771,7.9618771 0 0 1 7.961877,-7.96188 7.9618771,7.9618771 0 0 1 7.961877,7.96188 z" />
      <path
         id="rect1-5"
         style="fill:#e68369;fill-opacity:0.988235;stroke-width:9.2261;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:0;paint-order:fill markers stroke"
         d="m 59.178863,113.95217 h 63.014417 c 4.15832,0 7.50599,1.90314 7.50599,4.26713 v 7.07102 c 0,2.36399 -3.34767,4.26713 -7.50599,4.26713 H 59.178863 c -4.15832,0 -7.505993,-1.90314 -7.505993,-4.26713 v -7.07102 c 0,-2.36399 3.347673,-4.26713 7.505993,-4.26713 z m -11.6333,7.96188 a 7.9618771,7.9618771 0 0 1 -7.961877,7.96188 7.9618771,7.9618771 0 0 1 -7.961877,-7.96188 7.9618771,7.9618771 0 0 1 7.961877,-7.96188 7.9618771,7.9618771 0 0 1 7.961877,7.96188 z" />
    </g>
    <g
       id="layer4"
       transform="matrix(0.22733562,-0.19813109,0.19813109,0.22733562,66.273908,118.67182)">
      <path
         id="path12"
         style="fill:url(#linearGradient14);fill-opacity:1;stroke:none;stroke-width:0.97198;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:0;stroke-dasharray:none;stroke-opacity:1;paint-order:fill markers stroke"
         d="m 61.443709,215.7904 a 11.717514,11.717514 0 0 0 -0.04248,0.15207 11.717514,11.717514 0 0 0 9.077685,13.83456 11.717514,11.717514 0 0 0 13.799596,-8.77958 z" />
      <rect
         style="fill:url(#linearGradient6);stroke:#969696;stroke-width:0.750464;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:0;stroke-dasharray:none;stroke-opacity:1;paint-order:fill markers stroke"
         id="rect4"
         width="12.775372"
         height="17.796886"
         x="113.16803"
         y="102.44638"
         rx="0"
         ry="0"
         transform="rotate(12.845601)" />
      <path
         style="fill:url(#linearGradient2);stroke:#969696;stroke-width:4.85988;stroke-linecap:square;stroke-linejoin:round;stroke-miterlimit:0;stroke-dasharray:none;stroke-opacity:1;paint-order:fill markers stroke"
         id="path1"
         d="M 173.59536,47.255647 A 53.981506,53.981506 0 0 1 120.59382,102.04617 53.981506,53.981506 0 0 1 65.650365,49.203184 53.981506,53.981506 0 0 1 118.33437,-5.8927416 53.981506,53.981506 0 0 1 173.5823,46.631831"
         transform="rotate(12.845601)" />
      <rect
         style="fill:url(#linearGradient9);stroke:none;stroke-width:0.97198;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:0;stroke-dasharray:none;stroke-opacity:1;paint-order:fill markers stroke"
         id="rect7"
         width="23.601223"
         height="77.33165"
         x="107.79591"
         y="119.37928"
         transform="rotate(12.845601)" />
      <rect
         style="fill:#323232;fill-opacity:1;stroke:none;stroke-width:0.97198;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:0;stroke-dasharray:none;stroke-opacity:1;paint-order:fill markers stroke"
         id="rect10"
         width="23.593927"
         height="2.4178843"
         x="107.79429"
         y="119.37928"
         transform="rotate(12.845601)" />
    </g>
    <g
       id="layer2"
       transform="matrix(0.64031733,0.38057975,-0.38057975,0.64031733,106.98751,6.3516524)">
      <path
         id="rect3"
         style="fill:url(#linearGradient4);stroke-width:0.379052;stroke-miterlimit:0;paint-order:fill markers stroke"
         d="m 99.231858,166.31875 7.812002,9.30912 7.81164,-9.30913 z" />
      <rect
         style="fill:url(#linearGradient18);fill-opacity:1;stroke:none;stroke-width:0.379052;stroke-miterlimit:0;paint-order:fill markers stroke"
         id="rect2-9"
         width="15.62549"
         height="55.154213"
         x="99.231049"
         y="111.16447" />
      <path
         id="rect1-236"
         style="fill:#c85050;fill-opacity:1;stroke-width:0.379052;stroke-miterlimit:0;paint-order:fill markers stroke"
         d="m 102.10017,99.941335 c -1.57455,0 -2.842115,1.510525 -2.842115,3.386865 v 7.83648 h 15.598525 v 1.39802 c 0.016,-0.14578 0.0269,-0.29342 0.0269,-0.44455 v -8.78995 c 0,-1.87634 -1.26757,-3.386865 -2.84212,-3.386865 z" />
    </g>
  </g>
</svg>
'''
