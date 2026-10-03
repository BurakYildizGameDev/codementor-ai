using System;

public class Searcher {
    public static int BinarySearch(int[] arr, int target) {
        int low = 0;
        int high = arr.Length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) {
                return mid;
            }
            if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }
}
