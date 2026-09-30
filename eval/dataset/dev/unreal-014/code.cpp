#include "Squad.h"

void ASquad::RemoveDead()
{
    for (AActor* Member : Members)
    {
        if (!IsValid(Member))
        {
            Members.Remove(Member);
        }
    }
}
