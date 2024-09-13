import threading


def threaded(func):
    def wrapper(*args, **kwargs):
        try:
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            # thread.join()
        except Exception as e:
            print(f"Failed from threaded call! Exception: {e}")

    return wrapper
