function [ AP apavg allTestprob] = trainPrecMultiClassOld( trainmat,testmat,trainlabel,testlabel,feaName)
%TRAINPRECMULTICLASS
%   Multiclass svm training and calculate precision according to the
%       highest probability of each class
%   Using kernel SVM, trainmat and testmat are kernel matrix.
%   The label of the each class should be 1:n
%   trainmat:  n*n matrix
%   testmat:   t*n matrix, each row as a data point

trainSampleNumber = size(trainmat,1);
testSampleNumber = size(testmat,1);

classNumber = 20;

allTestprob = zeros(testSampleNumber,classNumber);

apavg = zeros(classNumber,1);

for i=1:classNumber
    svmTrainlabel = zeros(trainSampleNumber,1);
    svmTestlabel = zeros(testSampleNumber,1);
    svmTrainlabel = trainlabel(:,i);
    svmTestlabel = testlabel(:,i);
    model=svmtrain(svmTrainlabel,[(1:trainSampleNumber)' trainmat],'-c 4 -b 1 -t 4');
    [estlab,accur,prob]=svmpredict(svmTestlabel,[(1:testSampleNumber)' testmat],model,'-b 1');
    
    groundtruth=size(find(svmTestlabel==1),1);

    sc=zeros(1,testSampleNumber);
    for k=1:testSampleNumber
        if(estlab(k,1)==1)
            sc(1,k)=max(prob(k,:)');
        else
            sc(1,k)=min(prob(k,:)');
        end
    end
    %save(['/home/dq/ccv_and_journal_score/old_score/' feaName '_old' sprintf('%d',i) '.mat'],'sc');
    allTestprob(:, i) = sc';
    [score,in]=sort(sc,'descend');

    cutoff=0;
    mysum=0;
    for k=1:testSampleNumber
        if(svmTestlabel(in(k))==1)
            cutoff = cutoff+1;
            mysum=mysum+cutoff/double(k);
        end
    end

    apavg(i)=mysum/groundtruth;
    
    groundtruth=[];
    
end

AP=mean(apavg);

end

