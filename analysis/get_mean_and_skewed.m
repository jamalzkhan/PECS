function [ m, skewed_response ] = get_mean_and_skewed( response_times )
m = min(response_times);
skewed_response = response_times - m;
mea = mean(skewed_response);
end