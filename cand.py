from pkg_resources import resource_filename
from passporteye.util.ocr import ocr
from skimage.io import imread


# Smoke test for Tesseract OCR
def test_ocr():
    ocr_file = lambda fn, mode: ocr(imread(resource_filename('tests', 'data/%s' % fn)), mode)

    s = ocr_file('/home/hp/ocr/america.jpg', False)
    assert s.startswith('The (quick) [brown] {fox} jumps!\nOver the $43,456.78 <lazy> #90 dog\n')
    assert s.endswith('preguicoso.') or s.endswith('preguieoso.')  # NB: This actually depends on the version of Tesseract

    s = ocr_file('/home/hp/ocr/america.jpg', False)
    assert s.startswith('This is a lot of 12 point text to test the\nocr code and see if') or s.startswith('This is a lot of 12 point text to test the\ncor code and see if')
    assert s.endswith('The quick\nbrown dog jumped over the lazy fox.')
