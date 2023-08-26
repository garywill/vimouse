from heads import *
import g
exec(open('impo.py').read())





class WdApp(QApplication) :
    pub_show = pyqtSignal()
    pub_hide = pyqtSignal()
    pub_quit = pyqtSignal()
    
    def __init__(self, argv):
        super().__init__([])
        
        self.wd = TransparentWidget(argv[0], argv[1], argv[2], argv[3] )
        
        
    def hide(self):
        self.wd.hide()
        self.wd.refreshTimer.stop()
        
    def show(self):
        self.wd.refresh()
        self.wd.show()
        self.wd.refreshTimer.start()
        
    def slot_quit(self):
        self.wd.refreshTimer.stop()
        self.wd.close()
        self.quit()


class TransparentWidget(QWidget):
    def __init__(self, x, y, w, h):
        super().__init__()
        
        # https://doc.qt.io/qt-5.15/qt.html#WidgetAttribute-enum
        
        self.setWindowFlags(Qt.WindowTransparentForInput
                            |Qt.X11BypassWindowManagerHint
                            |Qt.WindowStaysOnTopHint
                            |Qt.FramelessWindowHint
                            # |Qt.WindowDoesNotAcceptFocus
                            |Qt.CoverWindow
                        )
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # self.setAttribute(Qt.WA_AlwaysStackOnTop, True)


        # # # 获取屏幕大小并设置窗口大小
        # screen = QGuiApplication.primaryScreen()
        # if screen is not None:
        #     rect = screen.availableGeometry()
        #     print(rect)
        #     self.setGeometry(rect)
            
        self.setGeometry(QRect(x,y,w,h))
        

        # 定时器每秒触发一次重绘
        self.refreshTimer = QTimer(self)
        self.refreshTimer.timeout.connect(self.refresh)
        self.refreshTimer.start(300)
        
        print('QWidget subclass __init__ finish')

    def refresh(self) :
        self.raise_()
        self.update()
        
    def paintLabel(self, text, x, y):
        qp = QPainter(self)
        
        qp.setFont ( QFont('Arial', g.fontsize, QFont.Bold) )
        
        metrics = qp.fontMetrics()
        
        w = metrics.width(text)
        h = metrics.height()
        # w=len(text)*8
        h=g.fontsize
        # print(w,h)
        w_ex = 1
        h_ex = 2
        
        ### pen外，brush内
        
        b_color = QColor(243,228,140, 180) #背景
        r_color = QColor(0,0,255,100) #框
        t_color=QColor(0,0,0, 200) # 字
        
        # 背景
        # qp.setPen(b_color) 
        qp.setBrush(b_color) 
        qp.fillRect( x-w//2-w_ex  , y-h//2-h_ex , w+2*w_ex, h+2*h_ex  , b_color )
        
        # 框
        qp.setPen(r_color)  
        qp.setBrush(Qt.transparent)  
        qp.drawRect( x-w//2-w_ex  , y-h//2-h_ex , w+2*w_ex, h+2*h_ex  )
        
        
        qp.setPen(QPen(t_color))
        qp.setBrush(QBrush(t_color))
        qp.drawText( x-w//2       , y+h//2      ,      text)
        
        
    def hideEvent(self, event):
        time.sleep(g.screenshotDelay/1000)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        wdW, wdH = self.width(), self.height()

        cell_width, cell_height = wdW // g.n_cols, wdH // g.n_rows
        pen = QPen(QColor(255,170,0, 127))
        painter.setPen(pen)
        # 绘制窗口最外边框矩形
        painter.drawRect(0, 0, wdW - 1, wdH - 1)
        

        if g.showingScreen == 'keys':
            cls = [ QColor(255, 255, 255, 127)  , QColor(255,170,0, 127), QColor(0,0,0, 127) ] 
            for ic in range(len(cls)) :
                cl = cls[ic]
                pen = QPen(cl)
                painter.setPen(pen)
                for i in range(1, g.n_rows):
                    y = i * cell_height + (ic-1)
                    painter.drawLine(0, y, wdW, y)
                for j in range(1, g.n_cols):
                    x = j * cell_width + (ic-1)
                    painter.drawLine(x, 0, x, wdH)
            
            for kpc in g.keypList :
                self.paintLabel(''.join(kpc['keyp']) ,  g.curCellX + kpc['cord'][0] , g.curCellY + kpc['cord'][1] )
                
                
                
        elif g.showingScreen == 'grid':
            pen = QPen(QColor(255,170,0, 200))
            painter.setPen(pen)
            letterH = int(cell_height * 0.5)
            for letter in g.cells :
                obj = g.cells [ letter ]
                x=obj['x']
                y=obj['y']
                w=obj['w']
                h=obj['h']
                painter.setBrush(QBrush(QColor(0,0,0, 0)))
                painter.drawRect(x, y, w, h)
                painter.setFont( QFont('Arial', letterH, QFont.Bold) )
                painter.setBrush(QBrush(QColor(255,170,0, 127)))
                painter.setPen(pen)
                painter.drawText(x + w//3 , y + h - h//4 , letter)
                


    # def bye(self):
    #     print("QWidget subclass bye()")
    #     self.refreshTimer.stop()
    #     self.close()
    #     QApplication.quit()
