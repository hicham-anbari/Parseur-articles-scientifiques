t = Time.now

tableau = []
for n in 0..10000
    a = rand 100
    tableau.push(a)
end

def insertion_sort(array)
    for i in 1...(array.length)
        j = i
        while j > 0
            if array[j-1] > array[j]
                temp = array[j]
                array[j] = array[j-1]
                array[j-1] = temp
            else
                break
            end
            j = j - 1
        end
    end
    return array
end


insertion_sort(tableau)

t1 = Time.now

tf = t1.to_f - t.to_f

print tf