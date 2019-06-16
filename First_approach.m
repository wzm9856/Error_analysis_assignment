conn = sqlite('homework.db');
data = fetch(conn,'SELECT * FROM teachers');
id=double(cell2mat(data(:,1)));
depId=double(cell2mat(data(:,2)));
paper=double(cell2mat(data(:,4)));
H=double(cell2mat(data(:,5)));
journal=double(cell2mat(data(:,6)));
confer=double(cell2mat(data(:,7)));
scie=double(cell2mat(data(:,8)));
ei=double(cell2mat(data(:,9)));
sciCite=double(cell2mat(data(:,10)));
highCite=double(cell2mat(data(:,11)));
en=double(cell2mat(data(:,12)));
cn=double(cell2mat(data(:,13)));
workAge=double(cell2mat(data(:,14)));
y2018=double(cell2mat(data(:,15)));
% load('matlab.mat');
a_cn=cn./workAge;
a_en=en./workAge;
a_confer=confer./workAge;
a_ei=ei./workAge;
a_journal=journal./workAge;
a_paper=paper./workAge;
a_sciCite=sciCite./workAge;
a_scie=scie./workAge;
% load('matlab.mat');

n=size(id,1);
x=[ones(n,1) a_paper a_journal a_confer a_scie a_ei a_cn a_en a_sciCite highCite workAge H];
y=y2018;
[S,U,Q,F]=calculate(x,y);
sigma2=Q/1320;

Pi=[];
Fi=[];
for a = 2:size(x,2)
    x1=[x(:,1:(a-1)) x(:,(a+1):size(x,2))];
    [~,Ui,~,~]=calculate(x1,y);
    Pi=[Pi U-Ui];
    Fi=[Fi Pi(a-1)/sigma2];
end
Pi
Fi