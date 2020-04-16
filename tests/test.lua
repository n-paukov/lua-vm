function sum(a, b)
    return a + b
end

function test_expressions()
    local a
    local b, c

    a = 10
    b = 15

    local t = sum(a, b)

    local table = {}
    table[10] = 20
    table[30] = 40
    table[50] = 50

    local d = table[50]

	return d
end


-- comment
function set_game_time(actor, npc, p)
	local real_hours = level.get_time_hours()
	local real_minutes = level.get_time_minutes()
	local hours = tonumber(p[1])
	local minutes = tonumber(p[2])
	if p[2] == nil then
		minutes = 0
	end
	local hours_to_change = hours - real_hours
	if hours_to_change <= 0 then
		hours_to_change = hours_to_change + 24
	end
	local minutes_to_change = minutes - real_minutes
	if minutes_to_change <= 0 then
		minutes_to_change = minutes_to_change + 60
		hours_to_change = hours_to_change - 1
	elseif hours == real_hours then
		hours_to_change = hours_to_change - 24
	end
	level.change_game_time(0,hours_to_change,minutes_to_change)
	level_weathers.get_weather_manager():forced_weather_change()
	surge_manager.get_surge_manager().time_forwarded = true
end
