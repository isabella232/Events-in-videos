function [ AP apavg prob] = ccvTrainOld(kernel,feaName)

trainlabel=load('../trainLabel.txt');
testlabel=textread('../testLabel.txt');

trainmat = kernel(1:4659,1:4659);
testmat = kernel(4660:end,1:4659);

gammaV = sum(sum(trainmat));
gammaV = gammaV/4659/4659;
gammaV = 1/gammaV;
trainmat = exp(-gammaV*trainmat);
testmat = exp(-gammaV*testmat);

[ AP apavg prob] = trainPrecMultiClassOld( trainmat,testmat,trainlabel,testlabel,feaName);

