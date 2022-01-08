import sys
sys.path.append('../src')
from Comic_Scraper.app import Comic
comic = Comic('life is strange')

def test_convert_space_to_dash():
    comic = Comic('life is strange')
    assert "life-is-strange" == comic.get_name()

