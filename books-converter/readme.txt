Convert English plain texts to multitask format for the classification
Run the script books_converter.py on the folder containing the documents you want to use to extract frame elements and convert them in a format readable by the classifier.

--folder: The input folder containing the books/document (plain txt, no metadata or tags)

--output: The output folder for the converted documents

--label: A short label used to assign an ID to the documents (so that later they can be matched with the metadata)

--books The script allows to merge multible books into a single file, setting the value to 1 create a file for each book

The script creates a -mapping file outside the output folder to map the document ID with the original books.

At line 41 change the seeds list file
```
with open ('SeedLists/seed-en-pos.txt','r') as fileSeeds:
```

At line 34 set the number of sentences to keep around each smell word. 3 means 3 before and 3 after, 7 sentences in total including the one with the seed
```
window_size = 3
```

If you are converting data for the v1 Bert classifier at line 117 replace
```
"\tO\tO\tO\tO\tO\tO\tO\tO\tO\tO\n"
```
with
```
"\tO\n"
```

Usage example:

```
python3 books_converter-10-filter.py --folder books_folder --output output_folder --label abc --books 1000
```