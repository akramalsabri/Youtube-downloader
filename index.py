from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import urllib.request
import pafy
import humanize

FROM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FROM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handal_Buttons()

    def Handel_UI(self):  # this function for UI
        self.setWindowTitle("Youtube Downloader")
        self.setFixedSize(687, 499)

    def Handal_Buttons(self):  # this function for Download button
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handal_Browse)
        self.pushButton_3.clicked.connect(self.Get_Youtube_Video)
        self.pushButton_7.clicked.connect(self.Download_youtube_video)
        self.pushButton_8.clicked.connect(self.save_Browse)
        self.pushButton_10.clicked.connect(self.save_Browse)
        self.pushButton_4.clicked.connect(self.get_youtube_Playlist)
        self.pushButton_9.clicked.connect(self.Download_youtube_playlist)



    def Handal_Browse(self):
        save_place = QFileDialog.getSaveFileName(self , caption="Save As", directory=".", filter="All Files (*.*)")
        text = str(save_place)
        name = (text[2:-1].split(',')[0].replace("'" , '' ))
        self.lineEdit_2.setText(name)

    def Handal_Progress(self ,blocknum ,blocksize ,totalsize):
        read = blocknum * blocksize

        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents() # solve not responding problem

    def Download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url , save_location , self.Handal_Progress)
        except Exception:
            QMessageBox.warning(self, "Download Error", "The Download Faild")
            return
        QMessageBox.information(self , "Download completed" , "The Download has been done successfully")
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

    def save_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select the directory")
        self.lineEdit_8.setText(save)
        self.lineEdit_10.setText(save)

    def Get_Youtube_Video(self):
        video_Link = self.lineEdit_7.text()
        v = pafy.new(video_Link)
        # print(v.title)
        # print(v.duration)
        # print(v.rating)
        # print(v.author)
        # print(v.length)
        # print(v.keywords)
        # print(v.thumb)
        # print(v.videoid)
        # print(v.viewcount)
        st = v.videostreams
        #print(st)
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data = "{} {} {} {}".format(s.resolution ,s.quality , s.extension ,size)
            self.comboBox_4.addItem(data)


    def Download_youtube_video(self):
        video_Link = self.lineEdit_7.text()
        save_location = self.lineEdit_8.text()
        v = pafy.new(video_Link)
        st = v.videostreams
        quality = self.comboBox_4.currentIndex()
        down = st[quality].download(filepath=save_location)
        QMessageBox.information(self, "Download completed", "The video has been downloaded successfully")

    def get_youtube_Playlist(self):
        Playlist_url = self.lineEdit_9.text()
        save_location = self.lineEdit_10.text()
        playlist = pafy.get_playlist(Playlist_url)
        videos = playlist['items']

        # create folder
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        #download platlist
        for video in videos:
            p = video['pafy']
            QApplication.processEvents()
            videostream = p.videostreams
            for s in videostream:
                size = humanize.naturalsize(s.get_filesize())
                data = "{} | {} | {} | {}".format(s.mediatype , s.quality ,s.extension, size)
                self.comboBox_5.addItem(data)
                quality = self.comboBox_5.currentIndex()
                down = videostream[quality].download(filepath=save_location , quiet=False)
                QMessageBox.information(self, "Download completed", "The video has been downloaded successfully")


    def Download_youtube_playlist(self):
        Playlist_url = self.lineEdit_9.text()
        save_location = self.lineEdit_10.text()
        playlist = pafy.get_playlist(Playlist_url)
        st = playlist.videostreams
        quality = self.comboBox_5.currentIndex()
        print(quality)
        #download_list =

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinite loop


if __name__ == '__main__':
    main()


#download link =  https://res.cloudinary.com/du8msdgbj/image/upload/l_watermark_346,w_690,h_700/a_ignore,w_690,h_700,c_pad,q_auto,f_auto/v1534917043/veyuxgcslrhjaekdqtxq.jpg

#DL = https://mail-attachment.googleusercontent.com/attachment/u/0/?ui=2&ik=2613751aa7&attid=0.2&permmsgid=msg-f:1698036201488853367&th=1790a2edbd7f2977&view=att&disp=safe&saddbat=ANGjdJ-XTvdDvrnkTPizt6iWFAqzlUhY4MNUXElA3_fS3eLbql-T4EaAd_r_O01dxIENvlrizlU0xHdjX8UHe5Fa7gfsZW0MUJXDPmECFFdyrQgtNp6HCCg3polUWGLZrauMb1ClCPmoEzHnEDg0lkSt7FHrKjU32itZ_vxYNBmDuS15XP6aloEes5tUZSw8kdD6IR_FnX4uES75cpWVw64cecibTvjQABUUNn5l8e62fQHI2wYRCiYRGjdsot8-xZxppKmflxDHNn6x7J4VLVnIF6LNmXMuZxPW1m61BRLvbh0P5zpUAWFhFoVYI01cGMfGMIb4p2WgQPrZXv5Otf-zpQhzlnIZwWTwyKwT4D6ED728bghMUci5o0JD8BmB2MFNn6aby_jaImSXoWx-7BiuN0x63RN2qyktWr4BhQBUHixzwVCzSsO6e4k5AKlAea-qHpLBbEg2uUrmFkTkdi_AEPrnB-RK_CS-wpVIkIPaXZv55RMT8bb66YAcTlZGp-7m3UY5cBbs5bzOzHiLGreBMZPqHA-rTJLYelGlLFevKJlg1zMFMgkammsMUNbDlGeBnTQ9cCqR35ztlHvJaxurkBmUQTXOvWQdhMxFSIIuzL3Nl1qUYALP5EnAF0avQQ5FuMFOOKjZ1fOjKqUkfdApUtTRE867Ug7f266As2IsJfgxopnqqKpdQBVfV7o

#Sublime Download link = https://download.sublimetext.com/Sublime%20Text%20Build%203211%20x64%20Setup.exe

#youtube link = https://www.youtube.com/watch?v=dFsULVxkXFs

#playlist link = https://www.youtube.com/watch?v=UD-MkihnOXg&list=PLU1ICX1TLRrD1VMWAnlaO2lIZ6wy5RxCw