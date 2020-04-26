function sum(a, b)
    function internal_function(a, b)
        return a + b
    end

    return internal_function(a, b)
end

function calculate_some_expr(a, b, c)
    t = sum(a, b)
    t = t - c

    return t
end

function print_interval(a, b, c)
    for number = 1, calculate_some_expr(a, b, c) do
        print("Iteration result is: ", number)
    end
end

print_interval(4, 6, 5)
