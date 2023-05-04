import argparse
import os
import re
from tqdm import tqdm


# path  = sys.argv[1]

parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="Input folder containing texts", metavar="FOLDER", required=True)
parser.add_argument("--output", help="Output folder", metavar="FOLDER", required=True)
parser.add_argument("--seeds", help="Seeds list file", required=True)
parser.add_argument("--books", help="Number of books to aggregate", metavar='N', type=int, default=100, required=False)
parser.add_argument("--window", help="Number of sentences to keep around each smell word", metavar='N', type=int, default=3, required=False)
parser.add_argument("--label", help="NLabel for the ID", type=str, required=True)

args = parser.parse_args()

path = args.folder
booksnumber = args.books
outPath = args.output
labelID = args.label
window_size = args.window
seedListFile = args.seeds

isExist = os.path.exists(outPath)
if not isExist:
    os.makedirs(outPath)

metaFileName = outPath
metaFileName = metaFileName.rstrip("/")
metaFileName = metaFileName.strip("\\")
metaFileName = "mapping-" + metaFileName + ".tsv"

book_counter = 0
out_name_counter = 0



def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

seed_list = []
# with open ('SeedLists/seed-en-pos.txt','r') as fileSeeds:
with open (seedListFile,'r') as fileSeeds:
    for line in fileSeeds:
        line = line.strip("\n")
        parts = line.split(",")
        for p in parts:
            seed_list.append(p.split("_")[0].lower())
print(seed_list)

for root, dirs, files in os.walk(path):
    print(root)
    for name in tqdm(files, total=len(files)):
        # for name in files:
            if name.endswith(".txt"):

                with open(os.path.join(root, name), 'r') as f:

                    book_counter += 1

                    with open(metaFileName, 'a') as metaOut:
                        metaOut.write(labelID + str(book_counter) + "\t" + name + "\n")

                    if book_counter % booksnumber == 0:
                        out_name_counter += 1

                    out_file_name = "books_merged_" + str(out_name_counter)

                    

                    outFile = open(os.path.join(outPath, out_file_name) + ".tsv", "a")
                    
                    book_sentences_list = []
                    tmp_sentence = []
                    index_to_print = dict()
                    for line in f:
                        line = line.strip("\n")
                        if len(line) < 1:
                            continue
                        accented_chars = 'àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ'
                        line = re.sub(r'\t', ' ', line)
                        line = re.sub(r'([^a-zA-Z' + accented_chars + '0-9])', ' \\1 ', line)
                        line = re.sub(' +', ' ', line)
                        parts = line.split(" ")
                        for p in parts:
                            if p == "":
                                continue
                            tmp_sentence.append(p)
                            if p == ".":
                                book_sentences_list.append(tmp_sentence)
                                tmp_sentence=[]
                        
                        #     tokenID = str(sentence_counter) + "-" + str(word_counter)
                        #     outFile.write(labelID + str(book_counter) + "\t" + tokenID + "\t-\t" + token + "\tO\tO\tO\tO\tO\tO\tO\tO\tO\tO\n")
                        #     # outFile.write(labelID + str(book_counter) + "\t" + tokenID + "\t-\t" + token + "\n")

                        #     word_counter += 1
                        #     if token == ".":
                        #         word_counter = 1
                        #         sentence_counter += 1
                        #         outFile.write("\n")
                    
                    
                    for sentence in enumerate(book_sentences_list):
                        lowlist= [x.lower() for x in sentence[1]]
                        overlap = intersection(lowlist,seed_list)
                        # overlap = intersection(sentence[1],seed_list)
                        if len(overlap) > 0:
                            for i in range(sentence[0]-window_size, sentence[0]+window_size+1):
                                index_to_print[i] = True
                                
                    for k in dict(sorted(index_to_print.items())):
                        sentence_counter = k
                        word_counter = 0
                        try:
                            for token in book_sentences_list[k]:
                                word_counter += 1
                                tokenID = str(sentence_counter) + "-" + str(word_counter)
                                outFile.write(labelID + str(book_counter) + "\t" + tokenID + "\t-\t" + token + "\tO\tO\tO\tO\tO\tO\tO\tO\tO\tO\n")
                            outFile.write("\n")
                        except:
                            out_of_range = True
                    
                    f.close()