
def chunks(iterable, chunkSize):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(iterable), int(chunkSize)):
        yield iterable[i:i + int(chunkSize)]
