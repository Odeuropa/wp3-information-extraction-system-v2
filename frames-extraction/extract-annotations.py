import sys
import os
import pandas as pd
import csv

# inputFile = sys.argv[1]
# path = sys.argv[1]

tokenID =1
textIndex = 3

# smell_word_tag = "Smell_Word"
# frameElements = ["Smell_Source","Quality"]

all_lines = []

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="Input folder containing texts", metavar="FOLDER", required=True)
parser.add_argument("--output", help="Output folder", required=True)
parser.add_argument("--smellwordtag", help="Smell word label", type=str, default ="Smell_Word")
parser.add_argument("--tags", help="List of labels comma separated", metavar="TASK",  type=str , default ="Smell_Source,Quality,Odour_Carrier,Evoked_Odorant,Location,Perceiver,Time,Circumstances,Effect")
parser.add_argument("--stopwords", help="Stopwordsfile",  type=str , default="", required=False)

args = parser.parse_args()


path = args.folder
outPath = args.output
stopwordpath = args.stopwords
smell_word_tag = args.smellwordtag
frameElements = args.tags.split(",")





def pocess_annotations(myAnnotations:list):
	annotationsDict = dict()
	outputDict = dict()

	s = [a for a in myAnnotations if smell_word_tag in " ".join(a)]

	# save all annotations in annotationsDict
	if len(s) == 0:
		return(None)
	annotationsDict[smell_word_tag] = s
	
	for f in frameElements:
		fe = [a for a in myAnnotations if f in " ".join(a)]
		annotationsDict[f] = fe

	#parse the annotations in annotationsDict merging tokens in the same span and puth them in outputDict
	
	# smell words:

	outputDict[smell_word_tag] = []
	firstID = int(annotationsDict[smell_word_tag][0][tokenID].split("-")[1])-1

	span = []
	for sw in annotationsDict[smell_word_tag]:

		myID = sw[tokenID].split("-")[1]
		myToken = sw[textIndex]

		if int(myID) == int(firstID)+1:
			span.append(myToken)
			firstID = myID

		else:	
			outputDict[smell_word_tag].append(" ".join(span))
			firstID = myID
			span = []
			span.append(myToken)

	outputDict[smell_word_tag].append(" ".join(span))

	
	#frame-elements

	

	for frameElement in frameElements:
		span = []
		outputDict[frameElement] = []
		if len(annotationsDict[frameElement]) == 0:
			continue
		
		firstID = int(annotationsDict[frameElement][0][tokenID].split("-")[1])-1
		
		for f in annotationsDict[frameElement]:

			myID = f[tokenID].split("-")[1]
			myToken = f[textIndex]
			
			if int(myID) == int(firstID)+1:
				span.append(myToken)
				firstID = myID
		
			else:	
				if " ".join(span).lower() not in spamList:
					outputDict[frameElement].append(" ".join(span))
				firstID = myID
				span = []
				span.append(myToken)

		if " ".join(span).lower() not in spamList:
			outputDict[frameElement].append(" ".join(span))
	
	return(outputDict)

def dictToString (myDict):
	myList = []
	myList.append("|".join(myDict[smell_word_tag]))
	for f in frameElements:
		myList.append("|".join(myDict[f]))
	return("\t".join(myList)+"\t")



spamList = []
if stopwordpath != "" :
	with open(stopwordpath, 'r') as file:
		for line in file:
			line = line.strip("\n")
			spamList.append(line)

annotations_list = []
sentence_list = []


# print("Book\tSmell_Word\tSmell_Source\tQuality\tFull_Sentence")

with open(outPath, "w") as outfile:
	


	for root, dirs, files in os.walk(path):
		for name in files:
			if name.startswith("."):
				continue
			if name.endswith(".eval"):
				continue
			counter = 0
			all_annotations_dict = dict()
			all_sentences_dict = dict()
			all_sentences_dict[0] = []
			all_titles_dict = dict()
			with open(os.path.join(root,name), 'r') as file:

				for line in file:
					line = line.strip()
					parts = line.split("\t")
					
					
					
					if line == "":
						counter += 1
						all_annotations_dict[counter] = annotations_list
						all_sentences_dict[counter] = sentence_list
						all_titles_dict[counter] = title
						sentence_list = []
						annotations_list = []

						continue

					title = parts[0]

					sentence_list.append(parts[textIndex])
					for p in parts[textIndex+1:]:
						if p != "O":
							annotations_list.append(parts)
							continue

				all_sentences_dict[counter+1] = []						

			for i in all_annotations_dict:
				# print(i)
				# print(i,all_titles_dict[i])
				# print(i,all_sentences_dict[i])
				# print(i,all_annotations_dict[i])
				# print()
				annotations_list = all_annotations_dict[i]
				
				sentence_list_before = all_sentences_dict[i-1]
				sentence_list = all_sentences_dict[i]
				sentence_list_after = all_sentences_dict[i+1]
				title = all_titles_dict[i]

				

				if len(annotations_list) > 1:
					
					dictAnnotations = pocess_annotations(annotations_list)
					
					if dictAnnotations != None:
						stringToPrint = dictToString(dictAnnotations)
						tmpString = title+"\t"+stringToPrint+" ".join(sentence_list_before)+"\t"+" ".join(sentence_list)+"\t"+" ".join(sentence_list_after)
						parts = tmpString.split("\t")
						all_lines.append(parts)
						if "\t\t" not in stringToPrint:
							tmpString = title+"\t"+stringToPrint+" ".join(sentence_list_before)+"\t"+" ".join(sentence_list)+"\t"+" ".join(sentence_list_after)
							parts = tmpString.split("\t")
							all_lines.append(parts)
							
				
				
myHeaderString = "Book\t"+smell_word_tag+"\t"+"\t".join(frameElements)+"\tSentenceBefore\tSentence\tSentenceAfter"
myHeader = myHeaderString.split("\t")
df = pd.DataFrame(all_lines)
df.columns=myHeader[:len(df.columns)]
df.to_csv(outPath, sep ='\t', index=False)
# df.to_csv(outPath, index=False)