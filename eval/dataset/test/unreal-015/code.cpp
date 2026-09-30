#include "Patroller.h"

void APatroller::AdvanceWaypoint()
{
    const FVector From = Waypoints[CurrentIndex]->GetActorLocation();
    const FVector To = Waypoints[CurrentIndex + 1]->GetActorLocation();
    MoveDirection = (To - From).GetSafeNormal();
    ++CurrentIndex;
}
