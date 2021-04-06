import json #2.0.9
import numpy as np

class Bot:
	
	def __init__(self):
		with open("D:\\TP_PROGS\\Projects\\TeProjSahara\\progs\\Sahara-System-For-Aiding-Visually-Impaired-master\\Sahara-System-For-Aiding-Visually-Impaired-master\\Server_side\\DataFiles\\corpus.json", "r") as f:
			self.corpus = json.loads(f.read())
			""" word: intent"""
			self.intents = ("TotalCash","ColorIdentification","BillReading","TextSummarization","BasicTextReading","DocumentClassification","CurrencyRecognition","Next","Stop","Object","Mask","Color")
			self.numFeatures = len(self.intents)
		
		
	def getIntent(self, inputText):
		'''
		A function that receives a inputText string and returns the most probable intent along with its probablilty
		e.g. "Identify the note" -> "CurrencyRecogntion, 0.9"
		'''
		print("inputText: ", inputText)
		totalCount =0
		probablityOfIntent = np.zeros(self.numFeatures)	
		words = inputText.lower().split()
		
		for word in words:
			intentIndex = self.corpus.get(word, None)
			print(intentIndex)
			if intentIndex!= None:
				totalCount+=1
				probablityOfIntent[self.corpus[word]] += 1
		print("intents:")
		print(probablityOfIntent)
		indexMax = np.argmax(probablityOfIntent)
		print(indexMax, self.intents[indexMax])
		print(totalCount)
		print(type(totalCount))
		if totalCount!=0 :
			return self.intents[indexMax], probablityOfIntent[indexMax]
		else:
			print("kuuch galat")
			return "I didnt catch what you said.", None
		
