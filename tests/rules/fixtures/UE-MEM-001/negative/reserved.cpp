#include "Grid.h"

void AGrid::BuildCells(int32 Count)
{
    TArray<FVector> Points;
    Points.Reserve(Count);
    for (int32 i = 0; i < Count; ++i)
    {
        Points.Add(FVector(i, 0, 0));
    }
    TArray<int32> Ids;
    Ids.Empty(Count);
    for (int32 i = 0; i < Count; ++i)
    {
        Ids.Add(i);
    }
}
