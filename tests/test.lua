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


local str = "Hello"
local str2 = ", world!"

local str3 = str..str2

print(str3)
print(sin(3.14159265 / 2))

print("Input A and B: ")
A = tonumber(read())
B = tonumber(read())

print(A + B)