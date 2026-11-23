def selection_sort(arr):
    n = len(arr)
    comparisons = 0
    assignments = 0
  
    for i in range(n - 1):
        min_index = i
        assignments += 1
  
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
                assignments += 1
  
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            assignments += 3
  
    return arr, comparisons, assignments

def insertion_sort(arr):
    n = len(arr)
    comparisons = 0
    assignments = 0
  
    for i in range(1, n):
        key = arr[i]
        assignments += 1
        j = i - 1
        assignments += 1 
  
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            assignments += 1
            j -= 1
            assignments += 1
  
        arr[j + 1] = key
        assignments += 1
  
    return arr, comparisons, assignments

A = [50, 80, 19, 86, 35, 7, 60, 48, 51]

print("=== Selection Sort ===")
sorted_sel, comp_sel, assign_sel = selection_sort(A.copy())
print("Відсортований масив:", sorted_sel)
print("Порівняння:", comp_sel)
print("Присвоєння:", assign_sel)

print("\n=== Insertion Sort ===")
sorted_ins, comp_ins, assign_ins = insertion_sort(A.copy())
print("Відсортований масив:", sorted_ins)
print("Порівняння:", comp_ins)
print("Присвоєння:", assign_ins)
