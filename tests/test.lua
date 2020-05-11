function sum(a, b)
    local p = 10

    function internal_function(a, b)
        p = 15

        return a + b
    end

    return internal_function(a, b)
end

function calculate_some_expr(a, b, c)
    local t = sum(a, b)
    t = t - c

    return t
end

function print_interval(a, b, c)
    for number = 1, calculate_some_expr(a, b, c) do
        print("Iteration result is: ", number)
    end
end

print_interval(4, 6, 5)

local var = tonumber(read())

if var > 10 then
    print("Variable 'var' is greater than 10 and has value " .. tostring(var))
end
