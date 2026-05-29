"""Examples demonstrating smart adaptive sort."""

import ordr

print("Smart Sort - Adaptive Algorithm Selection\n")
print("=" * 60)

# Small array - uses insertion sort
small = [5, 2, 8, 1, 9]
print("\nSmall array (uses insertion sort):")
print(f"Input:  {small}")
print(f"Output: {ordr.smart(small)}")

# Nearly sorted - uses timsort
nearly_sorted = list(range(100))
nearly_sorted[50], nearly_sorted[51] = nearly_sorted[51], nearly_sorted[50]
print("\nNearly sorted array (uses timsort):")
print(f"Input:  {nearly_sorted[:10]}... (swapped 2 elements)")
print(f"Output: {ordr.smart(nearly_sorted)[:10]}...")

# Many duplicates - uses timsort
duplicates = [5] * 30 + [1] * 30 + [3] * 30
print("\nMany duplicates (uses timsort):")
print(f"Input:  {duplicates[:15]}...")
print(f"Output: {ordr.smart(duplicates)[:15]}...")

# Random data - uses pdqsort
random_data = [9, 2, 7, 4, 1, 8, 3, 6, 5, 10]
print("\nRandom data (uses pdqsort):")
print(f"Input:  {random_data}")
print(f"Output: {ordr.smart(random_data)}")

# Large array - may use parallel sort
large = list(range(150000, 0, -1))
sorted_large = ordr.smart(large)
print("\nVery large array (may use parallel sort):")
print(f"Input:  {large[:10]}... (150,000 elements)")
print(f"Output: {sorted_large[:10]}...")
print("\n" + "=" * 60)
print("Smart sort automatically chooses the best algorithm!")
