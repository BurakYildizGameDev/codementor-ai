#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"
#include "TrackerActor.generated.h"

UCLASS()
class ATrackerActor : public AActor {
    GENERATED_BODY()

public:
    ATrackerActor();
    virtual void Tick(float DeltaTime) override;
};

ATrackerActor::ATrackerActor() {
    PrimaryActorTick.bCanEverTick = true;
}

void ATrackerActor::Tick(float DeltaTime) {
    Super::Tick(DeltaTime);
    TArray<AActor*> FoundActors;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AActor::StaticClass(), FoundActors);
}
