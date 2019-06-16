function[S, U, Q, F, b]=calculate(x,y)
n=size(x,1);
A=x'*x;
B=x'*y;
C=inv(A);
b=C*B;

S=sum((y-mean(y,1)).^2,1);
yhat=x*b;
U=sum((yhat-mean(y,1)).^2,1);
Q=sum((y-yhat).^2,1);
F=U/(size(x,2)-1)/Q*(n-size(x,2)-2);