function [ m, mu ] = get_min_and_parameter( data )

m = min(data);
new_data = data - min(data);
mu = fitdist(new_data, 'exponential');

end

