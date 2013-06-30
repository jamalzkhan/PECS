function [ ratio ] = find_cost_ratio_micro_large( param_small, param_large )
%FIND_COST_RATIO_MICRO_LARGE Summary of this function goes here
%   Detailed explanation goes here

micro_instance_hour = 0.025;
ex_instance_hour = 0.520;
micro_cost_per_request = param_small * (micro_instance_hour/60/60);
ex_cost_per_request = param_large * (ex_instance_hour/60/60);

ratio = micro_cost_per_request / ex_cost_per_request;

end

