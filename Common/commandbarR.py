from qfluentwidgets import CommandBar


class CommandBarR(CommandBar):
    def updateGeometry(self):
        self._hiddenWidgets.clear()
        self.moreButton.hide()

        visibles = self._visibleWidgets()
        h = self.height()
        w = self.width() - visibles[0].width() if visibles else self.width()
        for widget in visibles:
            widget.show()
            widget.move(w, (h - widget.height()) // 2)
            w -= (widget.width() + self.spacing())

        # show more actions button
        if self._hiddenActions or len(visibles) < len(self._widgets):
            self.moreButton.show()
            self.moreButton.move(w, (h - self.moreButton.height()) // 2)

        for widget in self._widgets[len(visibles):]:
            widget.hide()
            self._hiddenWidgets.append(widget)
