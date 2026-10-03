#include "CoreMinimal.h"
#include "Containers/Array.h"

void PopulateIndices(TArray<int32>& OutIndices, int32 Count) {
    for (int32 i = 0; i < Count; ++i) {
        OutIndices.Add(i * 3);
    }
}
