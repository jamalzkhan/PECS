function [ data ] = remove_n_max_elem( data, n )
%REMOVE_N_MAX_ELEM Summary of this function goes here
%   Detailed explanation goes here
    for i=1:n,
        m = max(data);
        data = data(data<m);
    end
end

