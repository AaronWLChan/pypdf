# pypdf
Python PDF Editor

Requires [Poppler](https://anaconda.org/conda-forge/poppler/files) to convert PDFs to image.

## Usage

### Merge Pages (by position)
python pypdf.py m 'PATH_TO_PDF,PATH_TO_PDF2' 'DESTINATION_PATH' pageNo


```python
python pypdf.py m 'a.pdf,b.pdf' 'c.pdf' 0
```
Note: You can only use this command with two PDFs.

### Merge Pages (append)
python pypdf.py ma 'PATH_TO_PDF,PATH_TO_PDF2...' 'DESTINATION_PATH'


```python
python pypdf.py ma 'a.pdf,b.pdf' 'c.pdf'
```

### Rotate Page
python pypdf.py r 'PATH_TO_PDF' pageNo degreesClockwise


```python
python pypdf.py r 'a.pdf' 0 90
```

### Delete Page
python pypdf.py d 'PATH_TO_PDF' pageNo


```python
python pypdf.py d 'a.pdf' 0
```

### Split PDF
python pypdf.py s 'PATH_TO_PDF' pageNo


```python
python pypdf.py d 'a.pdf' 0
```
Resulting files are named: Split 1.pdf & Split 2.pdf

### Swap Pages
python pypdf.py sw 'PATH_TO_PDF' pageNo pageNo


```python
python pypdf.py sw 'a.pdf' 0 1
```

### Convert to Image
python pypdf.py img 'PATH_TO_PDF' 'DESTINATION_DIRECTORY'


```python
python pypdf.py img 'a.pdf' '/Images'
```
