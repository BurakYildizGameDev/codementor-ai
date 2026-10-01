// EXPECT: 9
#include "Grid.h"

void AGrid::BuildCells(int32 Count)
{
    TArray<FVector> Points;
    for (int32 i = 0; i < Count; ++i)
    {
        Points.Add(FVector(i, 0, 0));
    }
    Cells = Points;
}
