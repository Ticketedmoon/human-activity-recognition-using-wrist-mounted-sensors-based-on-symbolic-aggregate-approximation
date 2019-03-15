# Gif Animation 
self.status_txt = QtWidgets.QLabel(self.frame)
self.status_txt.setGeometry(QtCore.QRect(10, 10, 300, 200))
self.status_txt.setAlignment(Qt.AlignCenter)
movie = QtGui.QMovie("walking.gif")
self.status_txt.setMovie(movie)
movie.start()
self.status_txt.setLayout(QtWidgets.QHBoxLayout())
# Gif Animation End

Primary Window Size: (1000, 600)