function [time]=piMC(N)
	tic
	n=0;

	for j=1:N
		x=rand;y=rand;
		if(x^2+y^2)<=1,n=n+1;end
	end
	mypi=4*gplus(n)/(numlabs*N);
	error=gop(@max, abs(pi-mypi));
	if(labindex == 1)
		fprintf('pi is about %E \n',mypi);
		fprintf('error is %E \n',error);
	end
time = toc;
