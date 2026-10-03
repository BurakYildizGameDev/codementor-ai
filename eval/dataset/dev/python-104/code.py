def reverse_array(arr: list[int]) -> list[int]:
    """İki işaretçi ile listeyi yerinde ters çevirir."""
    left = 0
    right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr
