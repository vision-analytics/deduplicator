# Project Details

**Method 1:** MD5 - Find duplicate files

**Method 2:** VGG16 + Annoy - Find similar images using feature extraction

<br/>
<hr/>
<br/>

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

````bash
pip3 install -r requirements.txt
````

<br/>
<hr/>
<br/>

## Usage

**methods:** "md5" or "vgg"

**img_dir:** "root dir of images"

**actions:** "move" / "copy"


````python
python3 main.py --method md5 --img_dir /home/image_dir/ --action copy

or

python3 main.py --method vgg --img_dir /home/image_dir/ --action copy
````

## Notebooks
````python
jupyter notebook

# if you are looking for exact match!
find-duplicate-files-md5.ipynb 

# if you are looking for similarity!
find-similar-images-feature-extraction-annoy.ipynb 
````

<br/>
<hr/>
<br/>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

<br/>
<hr/>
<br/>


## License
[MIT](https://choosealicense.com/licenses/mit/)

<br/>
<hr/>
<br/>

### Tested with following environments

Ubuntu 18.04 & python3.9.12

macOS Monterey 12.2.1 & python 3.9.12
