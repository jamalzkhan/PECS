function [ data ] = analysis( log_file )
    
data = parse_file(log_file);

% Do something with the data
hist(data, 1000)



end

