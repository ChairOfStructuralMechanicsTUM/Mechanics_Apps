close all;
clear all; clc;

n=100;
a=linspace(0,5,n);
b=linspace(0,10,n);
W= zeros(length(a), length(b));
for i= 1:length(a)
    for j= 1:length(b)
        W(i,j)= a(i)^-0.5 * (4-b(j))/a(i) * exp(-( (4-b(j))/a(i) )^2.0);
    end
end

[B,A]=meshgrid(b,a);
pcolor(B, A, W);
shading interp
xlabel ('b');
ylabel('a');
q=colorbar;
