#include "Squad.h"

void ASquad::Visible(const TArray<AActor*>& Actors, FNode* Node)
{
    TArray<AActor*> Out;
    for (AActor* Actor : Actors)
    {
        if (!Actor->IsHidden())
        {
            Out.Add(Actor);
        }
    }
    TArray<FNode*> Chain;
    while (Node != nullptr)
    {
        Chain.Add(Node);
        Node = Node->Next;
    }
    TSet<int32> Seen;
    for (int32 i = 0; i < 8; ++i)
    {
        Seen.Add(i);
    }
}
