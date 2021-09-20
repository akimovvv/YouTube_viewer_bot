from random import randint
from time import sleep

from selenium import webdriver
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from environs import Env

env = Env()
env.read_env()
# Create .env file in this project and create the variable YOUTUBE_API_KEY and put those your YOUTUBE_API_KEY
YOUTUBE_API_KEY = env.str('YOUTUBE_API_KEY')


class YouTube_viewer_app(App):
    # First main page here ypu should to input video url if video was find you get info about this video
    def build(self):
        al = AnchorLayout()
        bl = BoxLayout(orientation='vertical', size_hint=(.5, .5))
        lb1 = Label(text='Введите ссылку на видео (YouTube)', font_size=20)
        bl.add_widget(lb1)
        self.ti1 = TextInput(font_size=20)
        bl.add_widget(self.ti1)
        bt1 = Button(text='Найти', on_release=self.check_url)
        bl.add_widget(bt1)
        al.add_widget(bl)
        return al

    def check_url(self, instance):
        # This method check that video exist in youtube
        if str(self.ti1.text).startswith('https://www.youtube.com/watch?v='):
            try:
                global URL
                URL = self.ti1.text
                VIDEO_ID = URL[32:]
                search_video_result = requests.get(
                    f'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={VIDEO_ID}&key={YOUTUBE_API_KEY}').json()
                if int(search_video_result['pageInfo']['resultsPerPage']) == 0 and int(
                        search_video_result['pageInfo']['totalResults']) == 0:
                    self.ti1.text = 'Видео не найдено пожалуйста проверьте ссылку и введите заново!'
                else:
                    # pprint.pprint(search_video_result['items'][0]['snippet']['channelTitle'])
                    data = dict(channel_name=search_video_result['items'][0]['snippet']['channelTitle'],
                                video_title=search_video_result['items'][0]['snippet']['localized']['title'],
                                views_count=search_video_result['items'][0]['statistics']['viewCount'],
                                like_count=search_video_result['items'][0]['statistics']['likeCount'],
                                dislike_count=search_video_result['items'][0]['statistics']['dislikeCount'],
                                comment_count=search_video_result['items'][0]['statistics']['commentCount'],
                                video_duration=search_video_result['items'][0]['contentDetails']['duration'][
                                               2:].replace('H', ' час. ').replace('M', ' мин. ').replace('S', ' сек.'),
                                pub_date=search_video_result['items'][0]['snippet']['publishedAt'].replace('T',
                                                                                                           ' ').replace(
                                    'Z', '')
                                )
                    app.stop()
                    global video_info_page_app
                    video_info_page_app = Video_info_page_app(channel_name=data['channel_name'],
                                                              video_title=data['video_title'],
                                                              views_count=data['views_count'],
                                                              pub_date=data['pub_date'],
                                                              like_count=data['like_count'],
                                                              dislike_count=data['dislike_count'],
                                                              comment_count=data['comment_count'],
                                                              video_duration=data['video_duration']
                                                              )
                    video_info_page_app.run()
            except Exception:
                self.ti1.text = 'Извините что-то пошло не так перезагрузите приложение!'
        else:
            self.ti1.text = 'Неверная ссылка пожалуйста проверьте ссылку и введите заново!'


class Video_info_page_app(App):
    # Second page here yo can see video details (info)
    def __init__(self,
                 channel_name: str,
                 video_title: str,
                 views_count: str,
                 pub_date: str,
                 like_count: str,
                 dislike_count: str,
                 comment_count: str,
                 video_duration: str):
        App.__init__(self)
        self.channel_name = channel_name
        self.video_title = video_title
        self.views_count = views_count
        self.pub_date = pub_date
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.comment_count = comment_count
        self.video_duration = video_duration

    def build(self):
        al = AnchorLayout()
        bl = BoxLayout(size_hint=(0.9, 0.9))
        gl = GridLayout(rows=2)
        gl1 = GridLayout(cols=2, size_hint=(0.6, 0.7))
        gl2 = GridLayout(rows=2, size_hint=(0.2, 0.2), padding=20)
        gl1.add_widget(Label(text='Название канала -', font_size=20))
        gl1.add_widget(Label(text=self.channel_name, font_size=20))
        gl1.add_widget(Label(text='Название видео -', font_size=20))
        gl1.add_widget(Label(text=self.video_title, font_size=20))
        gl1.add_widget(Label(text='Кол-во просмотров -', font_size=20))
        gl1.add_widget(Label(text=self.views_count, font_size=20))
        gl1.add_widget(Label(text='Кол-во лайков -', font_size=20))
        gl1.add_widget(Label(text=self.like_count, font_size=20))
        gl1.add_widget(Label(text='Кол-во дизлайков -', font_size=20))
        gl1.add_widget(Label(text=self.dislike_count, font_size=20))
        gl1.add_widget(Label(text='Кол-во комментариев -', font_size=20))
        gl1.add_widget(Label(text=self.comment_count, font_size=20))
        gl1.add_widget(Label(text='Длительность видео -', font_size=20))
        gl1.add_widget(Label(text=self.video_duration, font_size=20))
        gl1.add_widget(Label(text='Дата публикации -', font_size=20))
        gl1.add_widget(Label(text=self.pub_date, font_size=20))
        gl2.add_widget(Button(text='Запустить бота', on_release=self.start_youtube_bot_viewer)),
        gl2.add_widget(Button(text='Назад', on_release=self.go_back_to_main_menu))
        gl.add_widget(gl1)
        gl.add_widget(gl2)
        bl.add_widget(gl)
        al.add_widget(bl)
        return al

    def go_back_to_main_menu(self, instance):
        # method go back to first page
        video_info_page_app.stop()
        app.run()

    def start_youtube_bot_viewer(self, instance):
        # method to go next page to get view quantity
        video_info_page_app.stop()
        global start_viewer_bot_app
        start_viewer_bot_app = Start_viewer_bot_app()
        start_viewer_bot_app.run()


class Start_viewer_bot_app(App):
    # here i how many views does he want to get
    def build(self):
        al = AnchorLayout()
        bl = BoxLayout(orientation='vertical', size_hint=(.5, .5))
        dropdown = DropDown()
        bl.add_widget(Label(text='Выберите какое кол-во просмотров вы хотите!', font_size=20))
        self.mainbutton = Button(text='Кол-во просмотров')
        for view_count in range(100, 1001, 100):
            btn = Button(text=f'Views {view_count}', size_hint_y=None, height=80)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.mainbutton.bind(on_release=dropdown.open)
        bl.add_widget(self.mainbutton)
        bl.add_widget(Button(text='Ок', on_release=self.start_process))
        al.add_widget(bl)
        return al

    def start_process(self, instance):
        # this method starting process
        if str(self.mainbutton.text[6:]).isdigit():
            start_viewer_bot_app.stop()
            global process_working_app
            process_working_app = Process_working_app(self.mainbutton.text[6:])
            process_working_app.run()
        else:
            self.mainbutton.text = 'Выберите число!'


class Process_working_app(App):
    # View starting process page
    def __init__(self, count_views):
        App.__init__(self)
        self.count_views = count_views

    def build(self):
        al = AnchorLayout()
        self.bl = BoxLayout(orientation='vertical', size_hint=(.5, .5))
        self.lb1 = Label(text='После нажатия процесс начнётся\nне выключайте компьютер и не закрывайте окно!',
                         font_size=20)
        self.bl.add_widget(self.lb1)
        self.bt = Button(text='Начать процесс', on_release=self.start_process)
        self.bl.add_widget(self.bt)
        al.add_widget(self.bl)
        return al

    def start_process(self, instance):
        browser = webdriver.Chrome(r'C:\Users\user\Downloads\chromedriver.exe')
        duration_to_watch = video_info_page_app.video_duration.split(' ')
        if len(duration_to_watch) == 4:
            video_duration_seconds = int(int(duration_to_watch[0]) * 60 + int(duration_to_watch[2]))
        elif len(duration_to_watch) == 6:
            video_duration_seconds = int(((int(duration_to_watch[0]) * 60) * 60) + (
                    int(duration_to_watch[2]) * 60) + int(duration_to_watch[4]))
        try:
            for i in range(int(self.count_views)):
                browser.get(URL)
                sleep(randint(1, 3))
                if i == 0:
                    browser.find_element_by_css_selector(
                        '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button').click()
                sleep(randint(int(video_duration_seconds * 0.2), video_duration_seconds))
            browser.quit()
            browser.close()
        except Exception:
            browser.quit()
            browser.close()
            process_working_app.stop()
            app.run()


if __name__ == '__main__':
    app = YouTube_viewer_app()
    app.run()
