# wp3-information-extraction-system-v2


## __Step 1 - Convert Books__

The script in he folder `books-converter` converts plain texts to the format used for the multitask classification.
Run the script `books_converter.py` on the folder containing the documents you want to use to extract frame elements and convert them in a format readable by the classifier.

`--folder`: The input folder containing the books/document (plain txt, no metadata or tags)

`--output`: The output folder for the converted documents

`--seeds`: The file containing the seeds list. E.g. 'SeedLists/seed-en-pos.txt'

`--books`: The script allows to merge multible books into a single file, setting the value to 1 create a file for each book. Default value is 100.

`--window`: The number of sentences to keep around each smell word. 3 means 3 before and 3 after. Default value is 3.

`--label`: A short label used to assign an ID to the documents (so that later they can be matched with the metadata)


The script creates a -mapping file outside the output folder to map the document ID with the original books.

Usage example:

```
python3 books_converter-10-filter.py --folder books_folder --output output_folder --seeds SeedLists/seed-en-pos.txt --label abc --books 1000
```

## __Step 2 - Smells Prediction__

The folder `run-predictions`  contains the classifier (`predict.py`) to extract the smell sources from the books converted in the previous step.

Before running the script download the model in your language form here: https://drive.google.com/drive/u/1/folders/1HRfiE3atNbXHIfj8mjXNiPJPZCxSmHky 
and move it in `run-predictions/models` folder.

The code has ben tested with python 3.8. To install the required packages, in `run-predictions` folder run:
```
pip install -r requirements.txt
```

The script takes as argument in order: `model`, `file to predict`, `output file` (containing the predictions)

Optional: `--device` to select the gpu to be used.

The models for each language are in the folder `models`.

The folder `test-files` contains a sample file for each language to test if the classifier works.

Usage example:
```
mkdir predictions
```

```
python3 predict.py models/fr.pt test-files/test-fr.tsv predictions/predictions-test-fr.tsv --device 0
```

__Disclaimer:__ *The multitask classifier uses machamp framework. The code in `run-predictions` contains selected parts of the framework, modified for the purpose of Odeuropa Project. If you need to use the framework get the official version at https://github.com/machamp-nlp/machamp*

## __Step 3 - Frames Extraction__

This `extract-annotations.py` script in `frames-extraction` folder extract the predictions from the output of the previous step providing a tsv file with all the frames and sentences that can be then uploaded in the knowledge graph.

`--folder`: the folder with the predictions from the classifier

`--output`: the output .tsv file


The code has ben tested with python 3.8. To install the required packages, in `frames-extraction` folder run:
```
pip install -r requirements.txt
```

Usage example:
```
python3 extract-annotations.py --folder ../run-predictions/predictions/ --output test-frames.tsv
```
