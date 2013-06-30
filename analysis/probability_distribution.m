%Write Mongo
%[mean, skewed] =  get_mean_and_skewed(csvread('mongo_x_write_5000.log'));
%skewed = remove_n_max_elem(skewed,20);
% disp(mean);
% [f,x] = hist(skewed,100);
% pd = fitdist(skewed,'exp');
% disp(pd)
% 
% 
% bar(x,f/trapz(x,f))
% hold on;
% r = [0:1e-6:5e-4]
% ys = pdf(pd,r);
% range = [0:1e-6:5e-4];
% plot(range,ys)


%Read Mongo

% [mean, skewed] =  get_mean_and_skewed(csvread('mongo_x_read_5000.log'));
% skewed = remove_n_max_elem(skewed,20);
% 
% disp(mean);
% [f,x] = hist(skewed,100);
% pd = fitdist(skewed,'exp');
% disp(pd)
% 
% bar(x,f/trapz(x,f))
% hold on;
% range = [0:1e-7:8.5e-5];
% ys = pdf(pd,range);
% plot(range,ys)

% Read Postgres
% [mean, skewed] =  get_mean_and_skewed(csvread('postgres_m_read_5000.log'));
% skewed = remove_n_max_elem(skewed,20);
% 
% disp(mean);
% [f,x] = hist(skewed,100);
% pd = fitdist(skewed,'exp');
% disp(pd)
% 
% bar(x,f/trapz(x,f))
% hold on;
% range = [0:1e-5:4e-3];
% ys = pdf(pd,range);
% plot(range,ys)

%Write Postgres
% [mean, skewed] =  get_mean_and_skewed(csvread('logs/postgres_m_write_5000.log'));
% skewed = remove_n_max_elem(skewed,20);
% range = [0:1e-4:6.5e-2];

% 
% [mean, skewed] =  get_mean_and_skewed(csvread('logs/webserver_m_get.log'));
% skewed = remove_n_max_elem(skewed,20);
% range = [0:1e-4:2e-3];


[mean, skewed] =  get_mean_and_skewed(csvread('logs/webserver_m_post.log'));
skewed = remove_n_max_elem(skewed,30);
range = [0:1e-4:8.5e-3];


disp(mean);
[f,x] = hist(skewed,100);
pd = fitdist(skewed,'exp');
disp(pd)

bar(x,f/trapz(x,f))
hold on;

ys = pdf(pd,range);
plot(range,ys)