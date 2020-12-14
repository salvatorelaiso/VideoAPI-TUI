from typing import Any, Callable

from valid8 import ValidationError

from consumer.domain import *
from consumer.menu import Menu, Entry, Description


class App:
    __line_separator = '_' * 50

    def __init__(self, key):
        builder = Menu.Builder(Description('Video API'), auto_select=lambda: self.__print_videos()) \
            .with_entry(Entry.create('1', 'View more details', on_selected=lambda: self.__print_video())) \

        if key is not None:
            self.__key = key
            builder.with_entry(Entry.create('2', 'My videos', on_selected=lambda: self.__print_own_videos()))

        builder.with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Quit...'), is_exit=True))
        self.__menu = builder.build()
        self.__videoApi = VideoAPI()

    def __print_videos(self) -> None:
        api: Optional[List[VideoDetails]] = self.__videoApi.fetch_videos()
        if api is None:
            print("Cannot retrieve data!")
            exit()
        print(self.__line_separator)
        fmt = '%3s %-18s %-10s'
        print(fmt % ('#', 'Title', 'Category'))
        videos: List[VideoDetails] = api
        for index in range(len(videos)):
            video = videos[index]
            print(fmt % (video.id, video.title, video.category.value))
        print(self.__line_separator)

    def __print_video(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0)
            return int(value)

        selected_id = self.__read('Index (0 to cancel)', builder)
        if selected_id == 0:
            print('Cancelled!')
            return
        print(self.__line_separator)
        api: Optional[VideoDetails] = self.__videoApi.fetch_video(selected_id)
        if api is None:
            print("Video not found!")
        else:
            video: VideoDetails = api
            fmt = '%3s %-10s %-18s %-30s %-10s %-10s'
            print(fmt % ('#', 'Title', 'Author', 'Description', 'Category', 'Views'))
            print(fmt % (video.id, video.title.value, video.author_name, video.description.value, video.category.value,
                         video.views.count))
        print(self.__line_separator)

    def __print_own_videos(self):
        api: Optional[List[VideoDetails]] = self.__videoApi.fetch_own_videos(key=self.__key)
        if api is None:
            print("Cannot retrieve data!")
            exit()
        print(self.__line_separator)
        fmt = '%3s %-18s %-30s %-10s %-10s'
        print(fmt % ('#', 'Title', 'Description', 'Category', 'Views'))
        videos: List[VideoDetails] = api
        for index in range(len(videos)):
            video = videos[index]
            print(fmt % (video.id, video.title.value, video.description.value, video.category.value, video.views.count))
        print(self.__line_separator)

    def __run(self) -> None:
        self.__menu.run()

    def run(self) -> None:
        self.__run()

    def __save(self) -> None:
        return

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)


