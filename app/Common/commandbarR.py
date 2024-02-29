from qfluentwidgets import CommandBar


class CommandBarR(CommandBar):
    """
    从右向左排列的命令栏
    """

    def updateGeometry(self):
        self._hiddenWidgets.clear()
        self.moreButton.hide()

        visibles = self._visibleWidgets()
        if self.suitableWidth() <= self.width():
            x = self.width() - self.contentsMargins().right() - self.suitableWidth()
        else:
            w = self.moreButton.width()
            for index, widget in enumerate(self._widgets):
                w += widget.width()
                if index > 0:
                    w += self.spacing()

                if w > self.width():
                    w -= widget.width()
                    break
            x = self.width() - w - self.contentsMargins().right()
        h = self.height()

        for widget in visibles:
            widget.show()
            widget.move(x, (h - widget.height()) // 2)
            x += (widget.width() + self.spacing())

        # show more actions button
        if self._hiddenActions or len(visibles) < len(self._widgets):
            self.moreButton.show()
            self.moreButton.move(x, (h - self.moreButton.height()) // 2)

        for widget in self._widgets[len(visibles):]:
            widget.hide()
            self._hiddenWidgets.append(widget)
