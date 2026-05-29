import ordr

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

sorted_arr = ordr.smart(arr)
print(f"Smart sort: {sorted_arr}")

print(f"PDQ sort: {ordr.pdq(arr)}")
print(f"Tim sort: {ordr.tim(arr)}")
print(f"Intro sort: {ordr.intro(arr)}")

large_arr = list(range(100000, 0, -1))
sorted_large = ordr.par_sort_unstable(large_arr)
print(f"Parallel sort: first 10 elements = {sorted_large[:10]}")

int_arr = [170, 45, 75, 90, 802, 24, 2, 66]
print(f"Radix sort: {ordr.radix(int_arr)}")

neg_arr = [-5, -1, -10, 0, 3, -2]
print(f"With negatives: {ordr.smart(neg_arr)}")

dup_arr = [5, 5, 5, 1, 1, 3, 3]
print(f"With duplicates: {ordr.smart(dup_arr)}")
