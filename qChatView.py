import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction,
                             QWidget, QLabel, QScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QLayout,
                             QGraphicsOpacityEffect,
                             )
from PyQt5.QtCore import (Qt, QAbstractAnimation, QPropertyAnimation,
                          QSequentialAnimationGroup, QEasingCurve,
                          )

default_style = """\
MyChat{
    border-radius: 10px;
    font: bold 14px;
    padding: 6px;
    background: lawngreen;

}
OtherChat{
/*    border: 2px solid black;*/
    border-radius: 10px;
    font: bold 14px;
    padding: 6px;
    background: white;
}
"""

class MyChat(QLabel):
    pass
class OtherChat(QLabel):
    pass

class Base(QWidget):
    def set_fadeout(self, wait_for_sec=7):
        opc = QGraphicsOpacityEffect(self)
        self.opc = opc
        self.setGraphicsEffect(opc)

        cue = QSequentialAnimationGroup()
        self.cue = cue
        cue.addPause(wait_for_sec*1000)

        # Fade-out
        anim = QPropertyAnimation(opc, b"opacity")
        self.anim = anim
        anim.setDuration(3000)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.InExpo)

        cue.addAnimation(anim)
        cue.finished.connect(self.deleteLater)
        cue.start(QAbstractAnimation.DeleteWhenStopped)

    @classmethod
    def auto_delete(cls, text, wait_for_sec=30, parent=None):
        me = cls(text, parent)
        me.set_fadeout(wait_for_sec=wait_for_sec)
        return me

class Mine(Base):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = MyChat(text, self)
        self.initUI()

    def initUI(self):
        self.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.MinimumExpanding
                )
            )
        align = QHBoxLayout(self)
        self.text.setWordWrap(True)
##        self.text.setSizePolicy(
##            QSizePolicy(
##                QSizePolicy.Minimum,
##                QSizePolicy.MinimumExpanding
##                )
##            )
        align.addSpacing(20)
        align.addStretch(0)
        align.addWidget(self.text)


class Other(Base):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = OtherChat(text, self)
        self.initUI()

    def initUI(self):
        self.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.MinimumExpanding
                )
            )
        align = QHBoxLayout(self)
        align.setSizeConstraint(QLayout.SetMaximumSize)
        self.text.setWordWrap(True)
##        self.text.setSizePolicy(
##            QSizePolicy(
##                QSizePolicy.ShrinkFlag | QSizePolicy.ExpandFlag,
####                QSizePolicy.Preferred,
##                QSizePolicy.MinimumExpanding
##                )
##            )
        align.addWidget(self.text)
        align.addStretch(0)
        align.addSpacing(20)

class ShowHistory(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
##        # prep
##        self.items = []
        self.t_mode = False
        self._auto_scroll = True
        # make parts
        self.initUI()

    def initUI(self):
        if not self.parentWidget(): self.resize(400,300)
##        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        # construct and set
        base = QWidget(self)
        self.base = base
        self.setWidgetResizable(True)
##        base.setMinimumWidth(280)
        base.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Maximum,
                QSizePolicy.MinimumExpanding
                )
            )
        margin = QVBoxLayout(base)
        margin.setSizeConstraint(QLayout.SetMaximumSize)
        scroll_layout = QVBoxLayout(base)
        self.scroll_layout = scroll_layout
        base.setLayout(margin)
        margin.addLayout(scroll_layout)
        scroll_layout.setSizeConstraint(QLayout.SetMaximumSize)
        margin.addStretch(20)
        # set
        self.setWidget(base)
        # set trigger
        vSB = self.verticalScrollBar()
        self.vSB = vSB
        vSB.rangeChanged.connect(self.scroll_to_bottom)

    def i_said(self, text, fade=-1):
        if fade > 0:
            chat = Mine.auto_delete(text, wait_for_sec=fade, parent=self.base)
        else:
            chat = Mine(text, self.base)
        self.scroll_layout.addWidget(chat)

    def they_said(self, text, fade=-1):
        if fade > 0:
            chat = Other.auto_delete(text, wait_for_sec=fade, parent=self.base)
        else:
            chat = Other(text, self.base)
        self.scroll_layout.addWidget(chat)

    def clear_posts(self):
        for c in self.base.children():
            if isinstance(c, Base): c.deleteLater()

    def transparent(self, t_mode):
##        fshape = QFrame.NoFrame if t_mode else QFrame.Box
##        self.setFrameShape(fshape)
        base = self.base
        base.setAutoFillBackground(t_mode)
        base.setAttribute(Qt.WA_NoSystemBackground, t_mode)
        base.setAttribute(Qt.WA_TranslucentBackground, t_mode)
        base.update()

    def scroll_to_bottom(self):
        if not self._auto_scroll: return
        vSB = self.verticalScrollBar()
        vSB.setValue(vSB.maximum())
        ### top = minimum()
        ### bottom = maximum()
        ### doclength = maximum() - minimum() + pageStep()


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.t_mode = False
        self._ontop = False
        self._auto_scroll = True
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Main Window")
        self.resize(400,300)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # construct
        self.history = ShowHistory(self)
        self.setCentralWidget(self.history)
        self.history.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                               QSizePolicy.MinimumExpanding
                                               )
                                   )
##        self.sw_transparent()
##        self.setWindowFlags(self.windowFlags()|Qt.CustomizeWindowHint)
        self.init_cmenu()

    def init_cmenu(self):
        # construct
        cmenu = QMenu(self)
        self.cmenu = cmenu
##        name = "withframe" if self.t_mode else "transparent"
        name = "transparent"
        sw_t = cmenu.addAction(name)
        sw_t.setCheckable(True)
        sw_t.setChecked(self.t_mode)
        sw_t.toggled.connect(self.sw_transparent)

        sw_s = cmenu.addAction("on top")
        sw_s.setCheckable(True)
        sw_s.setChecked(self._ontop)

        sw_s.toggled.connect(self.sw_auto_scroll)
        sw_s = cmenu.addAction("auto")
        sw_s.setCheckable(True)
        sw_s.setChecked(self._auto_scroll)
        sw_s.toggled.connect(self.sw_auto_scroll)

        self.extra_cmenu = cmenu.addSection("extra")

        close = cmenu.addAction("close")
        self.choice_close = close

    def sw_transparent(self):
        # keep current position
        pos = self.geometry()
        # switch opaque-transparent
        t_mode = not self.t_mode
        self.t_mode = t_mode
        self.history.transparent(t_mode)
##        self.setAttribute(Qt.WA_TranslucentBackground, t_mode)
        # frame includes border or background
        self.setWindowFlags(self.windowFlags() ^ Qt.FramelessWindowHint)
        # restore the position
        self.setGeometry(pos)  # frame operation moves the mainwindow
        self.show()

    def sw_ontop(self):
        self._ontop = not self._ontop
##        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)
##        # for not working
##        if self._ontop:
##            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
##        else:
##            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
    
    def sw_auto_scroll(self):
        self._auto_scroll = not self._auto_scroll
        self.history._auto_scroll = self._auto_scroll

    def contextMenuEvent(self, event):
        cmenu = self.cmenu
        close = self.choice_close
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
##        if action == sw_t:
##            self.sw_transparent()
        if action == close:
            self.close()

    def mousePressEvent(self, event):
        if Qt.LeftButton != event.button():
            return
        pos = event.pos()
        clicked = self.childAt(pos)
        if isinstance(clicked, QLabel):
            text = clicked.text()
            QGuiApplication.clipboard().setText(text)
            self.setWindowTitle(text)
        print("ouch")

    def addChat1(self, text, fade=-1):
        self.history.i_said(text, fade)
    def addChat2(self, text, fade=-1):
        self.history.they_said(text, fade)
    def clear_history(self):
        self.history.clear_posts()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(default_style)
    ex = MainWindow()
    ex.show()
    choice = (ex.addChat2, ex.addChat1)
    for k in range(100):
        choice[k&1]("test{:0>2}".format(k),fade=k+3)
##    sys.exit(app.exec_())
