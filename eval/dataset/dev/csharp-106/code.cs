using System;

public class ArrayHelper {
    public static int FindSum(int[] numbers) {
        int total = 0;
        for (int i = 0; i <= numbers.Length; i++) {
            total += numbers[i];
        }
        return total;
    }
}
