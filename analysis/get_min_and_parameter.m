function [ m, mu ] = get_min_and_parameter( data )
%GET_MIN_AND_PARAMETER Summary of this function goes here
%   Detailed explanation goes here

m = min(data);
new_data = data - min(data);
mu = fitdist(new_data, 'exponential');

end

