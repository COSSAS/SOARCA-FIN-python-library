from concurrent.futures import ThreadPoolExecutor


class DispatchQueue():

    def __init__(self):
        self.threadPoolExecutor = ThreadPoolExecutor(max_workers=1)

