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
r_cnen=en./(cn+en);
r_scie=scie./paper;
r_ei=ei./paper;
r_confer=confer./paper;
r_journal=journal./paper;
a_paper=paper./workAge;
r_sciCite=sciCite./scie;
% load('matlab.mat');
n=size(id,1);
x=[ones(n,1) a_paper r_confer r_scie r_ei r_cnen r_sciCite workAge H];
yes=isnan(x);
no=isinf(x);
for i = 1:size(x,1)
    for j = 1:size(x,2) 
        if yes(i,j) == 1
            x(i,j)=0;
        end
        if no(i,j) == 1
            x(i,j)=0;
        end
    end
end

y=y2018;
[S,U,Q,F,b]=calculate(x,y);
sigma2=Q/1323;

Pi=[];
Fi=[];
for a = 2:size(x,2)
    x1=[x(:,1:(a-1)) x(:,(a+1):size(x,2))];
    [~,Ui,~,~]=calculate(x1,y);
    Pi=[Pi U-Ui];
    Fi=[Fi Pi(a-1)/sigma2];
end
% Pi
% Fi