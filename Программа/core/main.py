import multiprocessing as multproc
from app import App


def app_loop():
    app = App()
    app.mainloop()


# Запуск
if __name__ == "__main__":
    procces_app = multproc.Process(target=app_loop)
    procces_app.start()
    procces_app.join()
