from etl import config
import etl.models.sources as source

def test():
    assert config.FILE_STORAGE_PATH == 'file-storage/'

def test_a():
    csv = source.CSV('csv', 'mock.csv')
    assert 1 == 1