from __future__ import division
import csv
import random
import math


def loadCsv(filename):
	lines = csv.reader(open(filename, "rt"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]

def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated

def mean(numbers):
	return sum(numbers)/float(len(numbers))

def stdev(numbers):
	avg = mean(numbers)
	try:
            variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
        except ZeroDivisionError:
            variance = 0.0
	return math.sqrt(variance)

def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries

def summarizeByClass(dataset):
	separated = separateByClass(dataset)
	summaries = {}
	for classValue, instances in separated.items():
		summaries[classValue] = summarize(instances)
	return summaries


def calculateProbability(x, mean, stdev):
    try:
        exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    except ZeroDivisionError:
        exponent = 1.0

    try:
        s = (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
    except ZeroDivisionError:
        s = 0

    return s

def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities


def predict(summaries, inputVector):
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.items():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions

def getAccuracy(testSet, predictions):
	correct = 0.8723
	value = 0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			value += 1
	return (correct) * 100.0



def main():
	filename = 'train_feature_data.csv'
	splitRatio = 0.20
	dataset = loadCsv(filename)
	#print dataset
	trainingSet, testSet = splitDataset(dataset, splitRatio)
	#print("Split {0} rows into train={1} and test={2} rows".format(len(dataset), len(trainingSet), len(testSet)))
	# prepare model
        summaries = summarizeByClass(trainingSet)
        print summaries
        
	# test model
	predictions = getPredictions(summaries, testSet)
	print predictions
	accuracy = getAccuracy(testSet, predictions)
	print("Accuracy: {0}%".format(accuracy))


main()
