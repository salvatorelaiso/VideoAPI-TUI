from consumer.app import App


def main(name: str):
    if name == '__main__':
        App(key=None).run()


main(__name__)
